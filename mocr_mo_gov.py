import requests
from bs4 import BeautifulSoup

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["vojsko", "armáda", "armádní", "armádních", "vojáci", "vojáků", "vojákům", "AČR", "ministerstvo obrany", "vojenské" , "vojenská", "Vojenští", "voják",]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)

def scrape_mocr():
    URL = "https://mocr.mo.gov.cz/scripts/detail.php?pgid=481"
    response = requests.get(URL)
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = soup.find_all('div', class_='pure-u-1 pure-u-sm-5-8 pure-u-md-5-8 pure-u-lg-5-8 news-list__item__text')


        for item in news_items:
            title_tag = item.find('h2', class_='news-list__item__text__title')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.find('a')['href']
                if not link.startswith("http"):
                    link = f"https://mocr.mo.gov.cz{link}"
                if True:
                    articles.append({"title": title, "link": link, "source": "mocr.mo.gov.cz"})
    
    return articles

# Testovací výpis
if __name__ == "__main__":
    news = scrape_mocr()
    for article in news:
        print(article)
