import requests
from bs4 import BeautifulSoup

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["vojsko", "armáda", "armádní", "armádních", "vojáci", "vojáků", "vojákům", "AČR", "ministerstvo obrany", "vojenské" , "vojenská", "Vojenští", "voják",]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_aktualne():
    URL = "https://zpravy.aktualne.cz/domaci/"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all("div", {"data-ga4-type": "article"})

        for item in news_items:
            title_tag = item.find("h3")
            link_tag = item.find("a")
            
            if title_tag and link_tag:
                title = title_tag.text.strip()
                link = link_tag["href"]
                if not link.startswith("http"):
                    link = f"https://zpravy.aktualne.cz{link}"
                if contains_keywords(title):
                    articles.append({"title": title, "link": link, "source": "aktualne.cz"})
    
    return articles

# Testovací výpis
if __name__ == "__main__":
    news = scrape_aktualne()
    for article in news:
        print(article)
