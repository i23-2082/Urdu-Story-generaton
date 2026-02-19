import time
import json
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

wait = WebDriverWait(driver, 10)

base_url = "https://www.urdupoint.com/kids/category/moral-stories-page{}.html"

all_stories = []

# -------- Loop Through All Pages --------
for page in range(1, 150):  # 1 to 149
    print(f"\n========== PAGE {page} ==========")

    driver.get(base_url.format(page))

    # Wait until stories load
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sharp_box")))
    time.sleep(2)

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

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "txt_detail")))
        time.sleep(2)

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

# -------- Save Everything --------
with open("all_urdu_moral_stories.json", "w", encoding="utf-8") as f:
    json.dump(all_stories, f, ensure_ascii=False, indent=4)

print("\n✅ ALL PAGES SCRAPED SUCCESSFULLY")
driver.quit()