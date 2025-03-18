from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["armáda", "vojáci", "AČR", "obrana", "ministerstvo obrany", "vojenské", "zásah", "cvičení", "voják", "střelbě"]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)


def scrape_idnes():
    """Scraper pro iDnes.cz pomocí Selenium"""
    options = Options()
    options.add_argument("--headless")  # Spustíme prohlížeč v neviditelném režimu
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Inicializace webdriveru
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

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
