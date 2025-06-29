import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords

def scrape():
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
    
    print(f"✅ Scraping seznamzpravy.cz dokončen, uloženo: {len(articles)} článků.")
    return articles
