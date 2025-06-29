import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords  # předpoklad: funkce filtruje články podle témat

def scrape():
    RSS_FEED_URL = "https://servis.idnes.cz/rss.aspx?c=zpravodaj"
    response = requests.get(RSS_FEED_URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")

        for item in items:
            # Filtrování podle <category domain="https://www.idnes.cz/zpravy/domaci">
            categories = item.find_all("category")
            is_domestic = any(
                cat.get("domain") == "https://www.idnes.cz/zpravy/domaci" or
                cat.text.strip().lower() == "zprávy - domácí"
                for cat in categories
            )
            if not is_domestic:
                continue

            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)

            # Filtrování podle klíčových slov
            if contains_keywords(title):
                articles.append({
                    "title": title,
                    "link": link,
                    "source": "idnes.cz"
                })

    print(f"✅ Scraping iDNES RSS (Zprávy - Domácí) dokončen, uloženo: {len(articles)} článků.")
    return articles

