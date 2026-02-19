import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------- Chrome Setup (VISIBLE) --------
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 15)  # Increased wait to 15 seconds
base_url = "https://www.urdupoint.com/kids/category/funny-stories-page{}.html"

# File to save data
output_file = "all_urdu_moral_stories.json"

# Load existing data if file exists
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        all_stories = json.load(f)
else:
    all_stories = []

# -------- Loop Through First 11 Pages --------
for page in range(1, 12):  # Pages 1 to 11
    print(f"\n========== PAGE {page} ==========")

    driver.get(base_url.format(page))

    # Wait until stories load, retry if needed
    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sharp_box")))
    except:
        print(f"No stories found on page {page}, retrying after 5 seconds...")
        time.sleep(5)
        continue

    time.sleep(3)  # extra wait to ensure complete page load

    story_elements = driver.find_elements(By.CLASS_NAME, "sharp_box")
    story_links = []

    for story in story_elements:
        link = story.get_attribute("href")
        if link:
            story_links.append(link)

    print(f"Found {len(story_links)} stories on page {page}")

    # -------- Visit Each Story --------
    for link in story_links:
        print("Opening:", link)
        driver.get(link)

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "txt_detail")))
        except:
            print("Story content not found, skipping...")
            continue

        time.sleep(2)  # wait to ensure story fully loads

        # ---- Title ----
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h2.urdu").text
        except:
            title = ""

        # ---- Subtitle ----
        try:
            subtitle = driver.find_element(By.CSS_SELECTOR, "p.txt_red").text
        except:
            subtitle = ""

        # ---- Date ----
        try:
            date = driver.find_element(By.CSS_SELECTOR, "p.art_info_bar").text
        except:
            date = ""

        # ---- Full Story ----
        try:
            container = driver.find_element(By.CLASS_NAME, "txt_detail")
            story_text = container.text.replace("(جاری ہے)", "")
        except:
            story_text = ""

        all_stories.append({
            "title": title,
            "subtitle": subtitle,
            "date": date,
            "content": story_text,
            "url": link
        })

        time.sleep(1)

    # -------- Save After Each Page --------
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Page {page} scraped and saved successfully!")

driver.quit()
print("\n🎉 FIRST 11 PAGES SCRAPED SUCCESSFULLY")