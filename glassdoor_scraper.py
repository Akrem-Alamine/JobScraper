import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import json
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

# Connect to an existing Chrome session started with remote debugging
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)
search_term = "internship"
location_term = "London"  # Example location
client = Groq(api_key=os.environ.get("OPENAI_API_KEY"))
try:
    # Use the unique id for the search input
    try:
        search_box = driver.find_element(By.ID, "searchBar-jobTitle")
    except Exception:
        search_box = None
    try:
        location_box = driver.find_element(By.ID, "searchBar-location")
    except Exception:
        location_box = None
    if search_box and location_box:
        search_box.clear()
        search_box.send_keys(search_term)
        location_box.clear()
        location_box.send_keys(location_term)
        location_box.send_keys(Keys.ENTER)
        print(f"Searched for: {search_term} in {location_term}")
    else:
        print("Search input or location input not found.")
except Exception as e:
    print(f"Error searching: {e}")

# Wait for results to load
print("Waiting 10 seconds for results to load...")
time.sleep(3)

# Select 'Most recent' from the sort dropdown if available
try:
    # Click the sort dropdown
    sort_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test='sortBy']")
    sort_btn.click()
    time.sleep(1)
    # Find and click 'Most recent' option
    recent_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Most recent')]")
    if recent_btns:
        recent_btns[0].click()
        print("Selected: Most recent")
    else:
        print("'Most recent' option not found.")
    time.sleep(2)
except Exception as e:
    print(f"Error selecting sort option: {e}")

# Scrape job cards
jobs_data = []
job_cards = driver.find_elements(By.CSS_SELECTOR, "li[data-test='jobListing']")
for card in job_cards:
    try:
        # Check and close job alert modal if it appears
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test='job-alert-modal-close']")
            close_btn.click()
            print("Closed job alert modal.")
            time.sleep(1)
        except Exception:
            pass
        # Click the card to open details
        driver.execute_script("arguments[0].scrollIntoView();", card)
        card.click()
        time.sleep(2)
        # Click 'Show more' if present
        try:
            show_more_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test='show-more-cta']")
            show_more_btn.click()
            time.sleep(1)
        except Exception:
            pass
        # Extract full job description
        try:
            desc_panel = driver.find_element(By.CSS_SELECTOR, "div[class*='JobDetails_jobDescription']")
            full_description = desc_panel.text.strip()
        except Exception:
            full_description = ""
        # Title
        try:
            title_el = card.find_element(By.CSS_SELECTOR, "a[data-test='job-title']")
            title = title_el.text.strip()
            link = title_el.get_attribute("href")
        except Exception:
            title = ""
            link = ""
        print(f"Title: {title}\nLink: {link}\nFull Description: {full_description}\n---")
        summary = ""
        # Summarize job description using Groq LLM
        if full_description:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": f"Summarize this job description: {full_description}"}],
                model="llama-3.1-8b-instant"
            )
            summary = response.choices[0].message.content
            print(f"Summary: {summary}\n---")
        job_info = {
            "title": title,
            "link": link,
            "description": full_description,
            "summary": summary
        }
        jobs_data.append(job_info)
    except Exception as e:
        print(f"Error parsing job card: {e}")

print(driver.title)

# Save jobs data to jobs.json
with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs_data, f, ensure_ascii=False, indent=2)

driver.quit()