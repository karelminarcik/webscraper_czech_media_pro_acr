import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords

def scrape():
    URL = "https://zpravy.aktualne.cz/rss/"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")
        items = soup.find_all("item")

        for item in items:
            title_tag = item.find("title")
            link_tag = item.find("link")
            category_tag = item.find("category")

            # Kontrola, že článek je v sekci Domácí
            if category_tag and category_tag.text.strip().lower() == "domácí":
                if title_tag and link_tag:
                    title = title_tag.text.strip()
                    link = link_tag.text.strip()
                    if contains_keywords(title):
                        articles.append({
                            "title": title,
                            "link": link,
                            "source": "aktualne.cz"
                        })
    print(f"✅ Scraping zpravy.aktualne.cz (RSS, sekce Domácí) dokončen, uloženo: {len(articles)} článků.")
    return articles
