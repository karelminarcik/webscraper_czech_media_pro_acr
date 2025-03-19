import schedule
import time
from main import main  # Importuje hlavní funkci scraperu

def job():
    print("🔍 Spouštím scraper...")
    main()
    print("✅ Hotovo! Články byly staženy a uloženy.")

# Naplánování úlohy na každý den v 9:00
schedule.every().day.at("12:47").do(job)

print("⏳ Čekám na naplánovaný čas...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Kontrola každou minutu
