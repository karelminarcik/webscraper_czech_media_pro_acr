from fastapi import FastAPI, Query, HTTPException  # Přidán import HTTPException
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from main import main
import shutil

app = FastAPI()

# 🔹 Povolíme přístup jen z konkrétní domény
origins = ["https://rentaacr.cz"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Povolí jen rentaacr.cz
    allow_credentials=True,
    allow_methods=["*"],  # Povolit všechny HTTP metody
    allow_headers=["*"],  # Povolit všechny hlavičky
)

def get_articles(source: str = None):
    """Načte články z databáze, včetně ID, volitelně filtrováno podle zdroje."""
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    if source:
        cursor.execute("SELECT id, title, link, source, date_added FROM articles WHERE source = ?", (source,))
    else:
        cursor.execute("SELECT id, title, link, source, date_added FROM articles ORDER BY date_added DESC")

    articles = [{"id": row[0], "title": row[1], "link": row[2], "source": row[3], "date_added": row[4]} for row in cursor.fetchall()]
    conn.close()
    return articles

@app.get("/")
def home():
    return {"message": "Vítejte v News API! Použijte /articles pro získání novinek."}

@app.get("/articles")
def read_articles(source: str = Query(None, description="Filtrujte podle zdroje (např. idnes.cz)")):
    return get_articles(source)

@app.get("/scrape")
def scrape(background_tasks: BackgroundTasks):
    """Spustí scraping na pozadí a uloží články do databáze."""
    background_tasks.add_task(main)
    return {"message": "Scraping byl spuštěn na pozadí."}

# 🔥 **Smazání článků podle ID nebo zdroje**
@app.delete("/articles")
def delete_articles(id: int = Query(None, description="ID článku ke smazání"), source: str = Query(None, description="Zdroj ke smazání")):
    """Smaže článek podle ID nebo všechny články ze zdroje."""
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    if id:
        cursor.execute("DELETE FROM articles WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return {"message": f"Článek s ID {id} byl smazán."}

    if source:
        cursor.execute("DELETE FROM articles WHERE source = ?", (source,))
        conn.commit()
        conn.close()
        return {"message": f"Všechny články ze zdroje '{source}' byly smazány."}

    conn.close()
    raise HTTPException(status_code=400, detail="Musíte zadat buď ID článku, nebo zdroj ke smazání.")

# kontrola zda a kde je nainstalovan chromium
@app.get("/check_chromium")
def check_chromium():
    chromium_path = shutil.which("chromium") or shutil.which("chromium-browser")
    
    # Ladicí výpis pro zjištění proměnných prostředí
    env_path = os.environ.get("PATH", "Nedefinováno")
    
    return {
        "chromium_path": chromium_path or "Chromium není nainstalováno",
        "env_PATH": env_path.split(":")  # Rozdělení PATH pro lepší čitelnost
    }
