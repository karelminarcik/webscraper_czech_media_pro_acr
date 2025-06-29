import requests
from bs4 import BeautifulSoup
from common.keywords import contains_keywords  # Ověř, že soubor existuje a funkce funguje

def scrape():
    URL = "https://www.novinky.cz/rss"
    articles = []

    try:
        response = requests.get(URL, timeout=10)
    except requests.RequestException as e:
        print(f"❌ Chyba při načítání RSS: {e}")
        return articles

    if response.status_code != 200:
        print(f"❌ Neúspěšná odpověď: {response.status_code}")
        return articles

    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")

    for item in items:
        try:
            title_tag = item.find("title")
            link_tag = item.find("link")

            title = title_tag.text.strip() if title_tag else ""
            link = link_tag.text.strip() if link_tag else ""

            # ✅ Filtrovat pouze články, které mají "/domaci/" v URL
            if "/domaci" in link and contains_keywords(title):
                articles.append({
                    "title": title,
                    "link": link,
                    "source": "novinky.cz"
                })
        except Exception as e:
            print(f"⚠️ Chyba při zpracování článku: {e}")

    print(f"\n✅ Scraping novinky.cz dokončen, uloženo: {len(articles)} článků.")
    return articles
