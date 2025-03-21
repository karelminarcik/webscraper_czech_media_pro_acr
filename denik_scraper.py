import requests
from bs4 import BeautifulSoup

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["NATO","armáda české republiky", "armáda","armádní", "vojáci","vojáků", "AČR", "obrana", "ministerstvo obrany", "vojenské", "Vojenští", "zásah", "cvičení", "voják", "střelbě"]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_denik():
    URL = "https://www.denik.cz/z_domova/"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all('a', class_='no-underline hover:text-primary-2 text-inky')

        for item in news_items:
            # Extrahování názvu článku z tagu <h2>
            title_tag = item.find('h2')
            if title_tag:
                title = title_tag.get_text(strip=True)
                # Získání odkazu z atributu href
                link = item['href']
                if not link.startswith("http"):
                    link = f"https://www.denik.cz{link}"
                # Filtrování článků na základě klíčových slov
                if contains_keywords(title):
                    articles.append({"title": title, "link": link, "source": "denik.cz"})
    
    return articles

print(scrape_denik())

