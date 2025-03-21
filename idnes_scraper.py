import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["armáda", "vojáci", "AČR", "obrana", "ministerstvo obrany", "vojenské", "zásah", "cvičení", "voják", "střelbě"]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def get_driver():
    """Inicializace WebDriveru pro Render.com"""
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Lepší výkon v omezeném prostředí
    options.add_argument("--remote-debugging-port=9222")  # Debugging pro server

    # 🔹 Použití cesty k předinstalovanému Chrome
    chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    options.binary_location = chrome_bin

    # 🔹 Automatická instalace Chromedriveru
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome(options=options)
    return driver

def scrape_idnes():
    """Scraper pro iDnes.cz pomocí Selenium"""
    driver = get_driver()
    URL = "https://www.idnes.cz/zpravy/domaci"
    driver.get(URL)

    time.sleep(3)  # Počkáme na načtení stránky

    articles = []
    news_items = driver.find_elements(By.CLASS_NAME, "art-link")

    for item in news_items:
        title = item.text.strip()
        link = item.get_attribute("href")
        # Kontrola klíčových slov
        if contains_keywords(title):
            articles.append({"title": title, "link": link, "source": "idnes.cz"})

    driver.quit()  # Zavřeme prohlížeč
    return articles

# Testování scraperu
if __name__ == "__main__":
    articles = scrape_idnes()
    for article in articles:
        print(article)
