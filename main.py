import sqlite3
from datetime import datetime
from seznam_scraper import scrape_seznam
from idnes_scraper import scrape_idnes
from irozhlas_sraper import scrape_irozhlas
from acr_mo_gov import scrape_acr
from denik_scraper import scrape_denik

# 🔹 Vytvoření databáze (pouze pokud neexistuje)
def create_db():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (  -- ✅ IF NOT EXISTS zabrání přepsání tabulky
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            source TEXT,
            date_added TEXT  -- Ukládáme datum jako text YYYY-MM-DD
        )
    """)

    conn.commit()
    conn.close()

# 🔹 Uložení článků do databáze
def save_to_db(articles):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")  # Aktuální datum

    for article in articles:
        try:
            cursor.execute("""
                INSERT INTO articles (title, link, source, date_added) 
                VALUES (?, ?, ?, ?)
            """, (article["title"], article["link"], article["source"], today_date))
        except sqlite3.IntegrityError:
            continue  # Pokud je článek už v DB, přeskočíme

    conn.commit()

    # ✅ Kontrola: Vypíšeme 5 nejnovějších článků
    cursor.execute("SELECT * FROM articles ORDER BY id DESC LIMIT 5")
    print("✅ Poslední články v databázi:")
    for row in cursor.fetchall():
        print(row)

    conn.close()

# 🔹 Hlavní funkce: Scrapování a ukládání do DB
def main():
    create_db()  # ✅ Už se nevytváří nová tabulka, pokud existuje

    all_articles = []
    all_articles.extend(scrape_irozhlas())
    all_articles.extend(scrape_idnes())
    all_articles.extend(scrape_seznam())
    all_articles.extend(scrape_acr())
    all_articles.extend(scrape_denik())

    save_to_db(all_articles)  # Uloží články do databáze

    print(f"Uloženo {len(all_articles)} článků do databáze.")

if __name__ == "__main__":
    main()
