import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords

def scrape():
    RSS_FEED_URL = "https://ct24.ceskatelevize.cz/rss/tema/vyber-redakce-84313"
    response = requests.get(RSS_FEED_URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")

        for item in items:
            # Filtrujeme jen položky s kategorií "Domácí"
            category = item.find("category", attrs={"domain": "https://ct24.ceskatelevize.cz/rubrika/domaci-5"})
            if not category:
                continue

            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)

            if contains_keywords(title):
                articles.append({
                    "title": title,
                    "link": link,
                    "source": "ct24.ceskatelevize.cz"
                })

    print(f"✅ Scraping ČT24 RSS (Domácí) dokončen, uloženo: {len(articles)} článků.")
    return articles

