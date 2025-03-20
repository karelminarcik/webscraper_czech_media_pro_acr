import requests
from bs4 import BeautifulSoup

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["evropa", "policie", "NATO","armáda české republiky", "armáda", "vojáci", "AČR", "obrana", "ministerstvo obrany", "vojenské", "zásah", "cvičení", "voják", "střelbě"]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_seznam():
    URL = "https://www.seznamzpravy.cz/sekce/domaci"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all("a", class_="mol-article-card__title-link")

        for item in news_items:
            title = item.text.strip()
            link = item["href"]
            if not link.startswith("http"):
                link = f"https://www.seznamzpravy.cz{link}"
            if contains_keywords(title):
                articles.append({"title": title, "link": link, "source": "seznamzpravy.cz"})
    
    return articles

