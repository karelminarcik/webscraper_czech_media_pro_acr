import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords

def scrape():
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
    print(f"✅ Scraping zpravy.aktualne.cz dokončen, uloženo: {len(articles)} článků.")
    return articles

