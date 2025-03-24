import requests
from bs4 import BeautifulSoup

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["NATO","armáda české republiky", "armáda","armádní", "armádních", "vojáci","vojáků", "AČR", "obrana", "ministerstvo obrany", "vojenské", "Vojenští", "zásah", "cvičení", "voják"]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_irozhlas():
    URL = "https://www.irozhlas.cz/zpravy-domov"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all("a", class_="b-article__link")

        for item in news_items:
            title = item.text.strip()
            link = item["href"]
            if not link.startswith("http"):
                link = f"https://www.irozhlas.cz{link}"
            if contains_keywords(title):
                articles.append({"title": title, "link": link, "source": "irozhlas.cz"})
    
    return articles


