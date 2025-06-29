import sqlite3
from datetime import datetime
from scrapers import acr_mo_gov, aktualne_sraper, ct24, denik_scraper, idnes_scraper, irozhlas_sraper, mocr_mo_gov, novinky_scraper, seznam_scraper, hospodarske_noviny
from database import create_db, save_to_db

# 🔹 Hlavní funkce: Scrapování dat z různých zdrojů a ukládání do databáze
def main():
    create_db()  # Vytvoří databázovou tabulku, pokud ještě neexistuje

    # Seznam scraperů, každý by měl mít metodu scrape() vracející seznam článků
    scrapers = [
        acr_mo_gov,
        aktualne_sraper,
        ct24,
        denik_scraper,
        idnes_scraper,
        irozhlas_sraper,
        mocr_mo_gov,
        novinky_scraper,
        seznam_scraper,
        hospodarske_noviny,
    ]

    all_articles = []  # Sem budeme ukládat všechny načtené články
    try:
        for scraper in scrapers:
            if hasattr(scraper, "scrape"):  # Ověříme, že scraper má metodu scrape()
                articles = scraper.scrape()  # Spustíme scraping
                if isinstance(articles, list):  # Zkontrolujeme, že vrací seznam článků
                    all_articles.extend(articles)  # Přidáme články do celkového seznamu
            else:
                print(articles)  # Pokud scraper nemá metodu scrape, vypíšeme chybu
    except Exception as e:
        print(f"❌ Chyba při scrapingu AČR: {e}")  # Zachytíme a vypíšeme chybu při scrapingu
    
    save_to_db(all_articles)  # Uložíme všechny články do databáze

    print(f"Uloženo {len(all_articles)} článků do databáze.")  # Informace o počtu uložených článků

if __name__ == "__main__":
    main()  # Spustíme hlavní funkci při přímém spuštění skriptu
