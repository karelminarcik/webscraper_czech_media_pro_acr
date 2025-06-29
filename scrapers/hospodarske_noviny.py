import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords

def scrape():
    RSS_FEED_URL = "https://domaci.hn.cz/?m=rss"
    response = requests.get(RSS_FEED_URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")

        for item in items:
            title = item.title.get_text(strip=True)
            link = item.link.get_text(strip=True)

            if contains_keywords(title):
                articles.append({
                    "title": title,
                    "link": link,
                    "source": "domaci.hn.cz"
                })

    print(f"✅ Scraping hospodarske noviny RSS (Domácí) dokončen, uloženo: {len(articles)} článků.")
    return articles
