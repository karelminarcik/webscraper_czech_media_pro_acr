from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

KEYWORDS = ["armáda", "vojáci", "AČR", "obrana", "ministerstvo obrany", "vojenské", "zásah", "cvičení", "voják", "střelbě"]

def contains_keywords(text):
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_idnes():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # 🔹 Automaticky detekuje Chromium
    possible_paths = ["/usr/bin/chromium", "/usr/bin/chromium-browser"]
    for path in possible_paths:
        if os.path.exists(path):
            options.binary_location = path
            break

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    URL = "https://www.idnes.cz/zpravy/domaci"
    driver.get(URL)
    time.sleep(3)

    articles = []
    news_items = driver.find_elements(By.CLASS_NAME, "art-link")

    for item in news_items:
        title = item.text.strip()
        link = item.get_attribute("href")
        if contains_keywords(title):
            articles.append({"title": title, "link": link, "source": "idnes.cz"})

    driver.quit()
    return articles

# Testování scraperu
if __name__ == "__main__":
    articles = scrape_idnes()
    for article in articles:
        print(article)
