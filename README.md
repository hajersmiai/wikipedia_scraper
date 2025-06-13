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

```bash
pip install requests beautifulsoup4
