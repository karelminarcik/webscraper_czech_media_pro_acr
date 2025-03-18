import requests
from bs4 import BeautifulSoup
import sqlite3
from seznam_scraper import scrape_seznam
from idnes_scraper import scrape_idnes
from irozhlas_sraper import scrape_irozhlas

# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = ["armáda", "vojáci", "AČR", "obrana", "ministerstvo obrany", "vojenské", "zásah", "cvičení", "voják", "střelbě"]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)



# 🔹 Vytvoření databáze
def create_db():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            source TEXT,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# 🔹 Uložení článků do databáze
def save_to_db(articles):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO articles (title, link, source) VALUES (?, ?, ?)
            """, (article["title"], article["link"], article["source"]))
        except sqlite3.IntegrityError:
            continue  # Pokud je článek už v DB, přeskočíme

    conn.commit()
    conn.close()

# 🔹 Hlavní funkce: Scrapování a ukládání do DB
def main():
    create_db()  # Vytvoří databázi, pokud neexistuje

    all_articles = []
    all_articles.extend(scrape_irozhlas())
    all_articles.extend(scrape_idnes())
    all_articles.extend(scrape_seznam())

    save_to_db(all_articles)  # Uloží články do databáze

    print(f"Uloženo {len(all_articles)} článků do databáze.")

if __name__ == "__main__":
    main()
