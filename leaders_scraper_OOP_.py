import requests as rq
from bs4 import BeautifulSoup as bs
import re
import json

class CountryLeadersAPI:
    def __init__(self, base_url):
        """
        Initialize the API client with a base URL.
        Also create a reusable requests.Session for Wikipedia scraping.
        """
        self.base_url = base_url.rstrip("/")  # Remove trailing slash if present
        self.cookies = self.get_cookie()      # Fetch initial cookie
        self.session = rq.Session()           # Session for Wikipedia requests (better performance)

    def get_status(self):
        """
        Check if the server is up and reachable.
        This helps verify that the base API is working.
        """
        req = rq.get(self.base_url + '/status')
        if req.status_code == 200:
            print("Server is up and running!")
        else:
            print(f"Server returned status code {req.status_code}. Something might be wrong.")

    def get_cookie(self):
        """
        Get a fresh cookie for authentication (if required by the API).
        If the cookie expires, this function can be called again.
        """
        return rq.get(self.base_url + '/cookie').cookies

    def get_first_paragraph(self, wikipedia_url):
        """
        Scrape the first suitable paragraph from a Wikipedia page.
        Uses the stored requests.Session to reuse the HTTP connection.
        Cleans the paragraph from references, pronunciation marks, and short parentheses.
        """
        # Download the page content
        response = self.session.get(wikipedia_url)
        soup = bs(response.content, 'html.parser')

        # Search for all paragraphs inside the main content section
        for p in soup.select("#mw-content-text p"):
            text = p.get_text(strip=True)

            # Basic filter: text must be long enough and meaningful
            if len(text) > 80 and "." in text and not text.startswith(("[", "(", "Coordinates")):
                # Remove [1], [note 2], etc.
                clean_text = re.sub(r'\[[^\]]*\]', '', text)
                # Remove pronunciations like (/ˈɪŋɡlænd/)
                clean_text = re.sub(r'\([^)]*[/ˈˌ][^)]*\)', '', clean_text)
                # Remove short parentheses, e.g., (born 1960)
                clean_text = re.sub(r'\(([^)]{1,25})\)', '', clean_text)
                # Replace multiple spaces with one space
                clean_text = re.sub(r'\s+', ' ', clean_text)
                return clean_text  # Return cleaned paragraph immediately

        # If no suitable paragraph is found
        return "No suitable paragraph found."

    def get_leaders(self) -> dict:
        """
        Retrieve leaders for all countries from the API,
        and enrich each leader's data with the first paragraph from Wikipedia.
        Handles expired cookies automatically.
        """
        # Check server status before proceeding
        self.get_status()

        # Request the list of countries
        countries = rq.get(self.base_url + "/countries", cookies=self.cookies).json()

        all_leaders = {}  # Dictionary to store all results

        # Loop through each country and get its leaders
        for country in countries:
            try:
                # Make API request to get leaders for this country
                response = rq.get(self.base_url + "/leaders", cookies=self.cookies, params={"country": country})

                # If cookie has expired or is invalid, get a new one and retry
                if response.status_code in [401, 403]:
                    print(f"Cookie expired for {country}, fetching new cookie...")
                    self.cookies = self.get_cookie()
                    response = rq.get(self.base_url + "/leaders", cookies=self.cookies, params={"country": country})

                # If it still fails, log and skip
                if response.status_code != 200:
                    print(f"Failed to get leaders for {country}: {response.status_code}")
                    all_leaders[country] = []
                    continue

                # Parse leaders list; handle API returning list or dict
                leaders = response.json() if isinstance(response.json(), list) else response.json().get("leaders", [])

                # For each leader, enrich with Wikipedia paragraph if available
                for leader in leaders:
                    wikipedia_url = leader.get("wikipedia_url")
                    if wikipedia_url:
                        leader['first_paragraph'] = self.get_first_paragraph(wikipedia_url)

                # Store leaders for this country
                all_leaders[country] = leaders

            except Exception as e:
                # In case of any unexpected error, log and store empty list for that country
                print(f"Error for {country}: {e}")
                all_leaders[country] = []

        return all_leaders

    def save(self, data, filename="leaders.json"):
        """
        Save the entire leaders dictionary to a JSON file.
        UTF-8 encoding ensures non-ASCII characters are preserved.
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")

    def read(self, filename="leaders.json"):
        """
        Read the leaders JSON file back into a dictionary.
        Print the country keys as a quick check.
        """
        with open(filename, "r", encoding="utf-8") as f:
            leaders_per_country = json.load(f)
        print(leaders_per_country.keys())
        return leaders_per_country


def main():
    """
    Example usage of the CountryLeadersAPI class.
    1. Initialize API client with base URL.
    2. Fetch leaders and enrich them with Wikipedia info.
    3. Save to file.
    4. Read back and print the country list.
    """
    api = CountryLeadersAPI("https://country-leaders.onrender.com")
    leaders_per_country = api.get_leaders()
    api.save(leaders_per_country)
    api.read("leaders.json")


if __name__ == "__main__":
    main()
