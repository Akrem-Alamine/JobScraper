# Job Scraping Project: Glassdoor, LinkedIn, Welcome to the Jungle, Indeed

This project scrapes job listings from multiple websites, starting with Glassdoor. Future support for LinkedIn, Welcome to the Jungle, and Indeed is planned.

## What's New
- Automatic 10-second wait for results to load (no manual input required)
- Summarizes job descriptions using Groq LLM (with a supported model, e.g., llama-3-8b-8192)
- Handles and closes modal dialogs automatically during scraping
- Saves results in a structured jobs.json file (title, link, summary)

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
4. Add your OPENAI_API_KEY to the .env file.
5. Run the scraper:
   ```bash
   python glassdoor_scraper.py
   ```

## Committing and Pushing Changes
1. Add all changes:
   ```bash
   git add .
   ```
2. Commit with a message:
   ```bash
   git commit -m "Update: Groq LLM summarization, modal handling, auto-wait, structured JSON output"
   ```
3. Push to your remote repository:
   ```bash
   git push
   ```

## Notes
- This tool uses browser automation to read publicly visible pages. Glassdoor may change HTML and deploy bot protection; selectors may need updates.
- Respect Glassdoor’s Terms of Service and robots.txt. Use for personal, non-commercial research unless you have permission.
- Future versions will add support for LinkedIn, Welcome to the Jungle, and Indeed.