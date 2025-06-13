# wikipedia_scraper
Wikipedia Scraper
# Country Leaders Scraper

This project provides a Python-based scraper and API client that fetches the current leaders of countries. It combines data from an API (`https://country-leaders.onrender.com`) and enriches the information by scraping Wikipedia to get additional personal details and introductory paragraphs about each leader.

---

## Features

- Fetches the list of countries from the API.
- Retrieves current leaders for each country from the API.
- For each leader, scrapes their Wikipedia page to extract a clean first paragraph summary.
- Uses a single HTTP session for Wikipedia requests to optimize performance.
- Handles expired API cookies by refreshing them automatically.
- Saves the collected data locally as a JSON file.
- Provides functions to load and read the saved JSON data.

---

## Versions

This repository includes **two versions** of the scraper for learning purposes:

- `leaders_scraper.py`: a simple version implemented using standalone functions for clear, step-by-step logic.
- `leaders_scraper_OOP.py`: an object-oriented version that wraps the same functionality in a clean, reusable Python class.

You can run either version depending on your preference for procedural or OOP style.

---
## Requirements

- Python 3.7+
- `requests` library
- `beautifulsoup4` library

Install dependencies with:
    pip install requests beautifulsoup4
    
## How to Use

- Clone or download this repository.

- Choose the version you want to run:

    Simple version:

        python leaders_scraper.py

    Object-Oriented version:

        python leaders_scraper_OOP.py

- The script will:

    Check the API status.

    Retrieve the list of countries.

    For each country, get its leaders from the API.

    Scrape Wikipedia for a short bio paragraph about each leader.

    Save all data to leaders.json.

    Print the list of countries found in the saved data.

## Code Structure

- Functions & Methods:

    get_leaders() / get_all_leaders(): Fetch countries and leaders, enrich with Wikipedia summaries.

    get_first_paragraph(): Scrape the first informative paragraph from a Wikipedia page.

    save(): Save the collected data to a JSON file.

    read(): Read and print the saved JSON data.

    Classes:
    In the OOP version, all related functions are encapsulated in a LeaderScraper class.

- Notes

    Wikipedia scraping uses CSS selectors to extract the first paragraph from the main content.

    The script automatically refreshes expired cookies when needed.

    A persistent requests.Session() is used for Wikipedia requests to improve efficiency.

## Potential Improvements

- Add command-line arguments for flexible configuration.

- Extend Wikipedia scraping to extract more structured data.

- Implement logging and error handling with log files.

- Use multi-threading or async requests for faster scraping.


