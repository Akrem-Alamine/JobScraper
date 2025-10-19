# Job Scraping Project: Glassdoor, LinkedIn, Welcome to the Jungle, Indeed

This project aims to scrape job listings from multiple websites, starting with Glassdoor. Future support for LinkedIn, Welcome to the Jungle, and Indeed is planned.

## Current Status: Glassdoor Scraper
- Scrapes internship/job listings from Glassdoor using Selenium and Chrome remote debugging.
- Extracts job title, link, and full description.
- Results are printed to the console (future: export to CSV/JSON).

## Setup
1. Python 3.9+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Chrome and start it with remote debugging enabled:
   ```bash
   chrome.exe --remote-debugging-port=9222
   ```
4. Run the scraper:
   ```bash
   python glassdoor_scraper.py
   ```

## Notes
- This tool uses browser automation to read publicly visible pages. Glassdoor may change HTML and deploy bot protection; selectors may need updates.
- Respect Glassdoor’s Terms of Service and robots.txt. Use for personal, non-commercial research unless you have permission.
- Future versions will add support for LinkedIn, Welcome to the Jungle, and Indeed.