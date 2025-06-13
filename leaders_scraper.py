import requests as rq            # Import requests library, aliased as rq for HTTP requests
from bs4 import BeautifulSoup as bs  # Import BeautifulSoup for HTML parsing, aliased as bs
import re                       # Import regex library for text cleaning
import json                     # Import JSON library for saving and loading JSON files

def get_leaders() -> dict:
    url = "https://country-leaders.onrender.com"  # Base API URL
    
    # Make a GET request to the /status endpoint to check if the server is up
    req = rq.get(url + '/status')
    
    # If server responds with status code 200 (OK)
    if req.status_code == 200:
        print("Server is up and running!")  # Inform user the server is reachable
    else:
        # If status code is different, warn user something might be wrong
        print(f"Server returned status code {req.status_code}. Something might be wrong.")
    
    # Get a cookie from the /cookie endpoint, needed for authenticated requests
    cookies = rq.get(url + '/cookie').cookies
    
    # Request the list of countries from the /countries endpoint using the cookie
    countries = rq.get(url + "/countries", cookies=cookies).json()
    
    # Initialize a dictionary to hold all leaders per country
    all_leaders = {}
    
    # Create a single HTTP session for Wikipedia scraping (efficient connection reuse)
    with rq.Session() as wiki_session:
        # Loop through each country in the list
        for country in countries:
            try:
                # Request the leaders of the current country from the /leaders endpoint with cookie
                response = rq.get(url + "/leaders", cookies=cookies, params={"country": country})
                
                # If the server responds with 401 or 403, the cookie might be expired or invalid
                if response.status_code in [401, 403]:
                    print(f"Cookie expired for {country}, fetching new cookie...")
                    # Request a new cookie
                    cookies = rq.get(url + "/cookie").cookies
                    # Retry the leaders request with the new cookie
                    response = rq.get(url + "/leaders", cookies=cookies, params={"country": country})
                
                # If after retrying, the response code is not 200, log the failure and continue
                if response.status_code != 200:
                    print(f"Failed to get leaders for {country}: {response.status_code}")
                    # Store empty list for this country in the result dictionary
                    all_leaders[country] = []
                    continue  # Move on to the next country
                
                # Parse the JSON response; handle cases where API returns a list or a dict with 'leaders' key
                leaders = response.json() if isinstance(response.json(), list) else response.json().get("leaders", [])
                
                # For each leader in the list, check if a Wikipedia URL is provided
                for leader in leaders:
                    wikipedia_url = leader.get("wikipedia_url")
                    if wikipedia_url:
                        # If yes, scrape the first relevant paragraph from the Wikipedia page
                        leader['first_paragraph'] = get_first_paragraph(wikipedia_url, wiki_session)
                
                # Store the enriched leaders list under the current country key
                all_leaders[country] = leaders
            
            except Exception as e:
                # Catch any unexpected exceptions during processing and log them
                print(f"Error for {country}: {e}")
                # Save an empty list in case of failure to not lose the key
                all_leaders[country] = []
        
    
    # Return the dictionary containing leaders info for all countries
    return all_leaders

""" 
Using a single requests.Session is best practice when doing multiple requests to the same website (Wikipedia here).
It reuses TCP connections internally, which reduces latency and makes scraping faster and more reliable.
"""
def get_first_paragraph(wikipedia_url, session):
    # Fetch the Wikipedia page content using the provided session to benefit from connection reuse
    soup = bs(session.get(wikipedia_url).content, 'html.parser')
    
    # Iterate over all paragraph (<p>) elements inside the main content div with id='mw-content-text'
    for p in soup.select("#mw-content-text p"):
        # Extract text from the paragraph and strip whitespace
        text = p.get_text(strip=True)
        
        # Only consider paragraphs longer than 80 characters that contain a period, and exclude certain starts
        if len(text) > 80 and "." in text and not text.startswith(("[", "(", "Coordinates")):
            # Remove references like [1], [note 2], etc. using regex
            clean_text = re.sub(r'\[[^\]]*\]', '', text)
            # Remove pronunciation parts inside parentheses containing '/' or 'ˈ' or 'ˌ'
            clean_text = re.sub(r'\([^)]*[/ˈˌ][^)]*\)', '', clean_text)
            # Remove short parenthetical info such as definitions or years (max 25 characters inside parentheses)
            clean_text = re.sub(r'\(([^)]{1,25})\)', '', clean_text)
            # Replace multiple spaces with a single space
            clean_text = re.sub(r'\s+', ' ', clean_text)
            # Return the cleaned paragraph text as soon as one valid paragraph is found
            return clean_text
    
    # Return this string if no suitable paragraph could be found on the page
    return "No suitable paragraph found."

def save(leaders_per_country):
    # Open a file named 'leaders.json' for writing in UTF-8 encoding
    with open("leaders.json", "w", encoding="utf-8") as file:
        # Write the dictionary to JSON with pretty indentation and UTF-8 support
        json.dump(leaders_per_country, file, ensure_ascii=False, indent=2)

def read(leaders):
    # Open the JSON file in read mode with UTF-8 encoding
    with open(leaders, "r", encoding="utf-8") as f:
        # Load the JSON data back into a Python dictionary
        leaders_per_country = json.load(f)
    # Print the dictionary keys, which correspond to country names, as a quick check
    print(leaders_per_country.keys())

# Call get_leaders to fetch all leaders data enriched with Wikipedia paragraphs
leaders_per_country = get_leaders()
# Save the fetched data to a local JSON file
save(leaders_per_country)
# Specify the filename to read from
leaders = "leaders.json"
# Read and print the keys from the saved JSON file
read(leaders)
