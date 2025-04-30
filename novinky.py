import requests
from bs4 import BeautifulSoup

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["vojsko", "armáda", "armádní", "armádních", "vojáci", "vojáků", "vojákům", "AČR", "ministerstvo obrany", "vojenské" , "vojenská", "Vojenští", "voják",]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_novinky():
    URL = "https://www.seznam.cz"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        boxik = soup.find("div", id="boxik-26")
        
        if boxik:
            news_items = [h3 for div in boxik.find_all("div", class_="font-14 article__text-box") for h3 in div.find_all("h3")]

            for item in news_items:
                # Najít <a> tag v každém článku
                a_tag = item.find('a')

                # Získání odkazu a titulku
                if a_tag:  # Zajistíme, že <a> tag existuje
                    link = a_tag['href']
                    title = a_tag.get_text()

                    # Oprava linku, pokud nezačíná 'http'
                    if not link.startswith("http"):
                        link = f"https://www.seznamzpravy.cz{link}"

                    # Pokud titul obsahuje klíčová slova, přidáme článek do seznamu
                    if contains_keywords(title):
                        articles.append({"title": title, "link": link, "source": "novinky.cz"})
    
    return articles

# Testování scraperu
if __name__ == "__main__":
    articles = scrape_novinky()
    for article in articles:
        print(article)  # Zobrazení informací o článcích
