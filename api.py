from fastapi import FastAPI, Query
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    """Načte články z databáze, volitelně filtrováno podle zdroje."""
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    if source:
        cursor.execute("SELECT title, link, source FROM articles WHERE source = ?", (source,))
    else:
        cursor.execute("SELECT title, link, source FROM articles")

    articles = [{"title": row[0], "link": row[1], "source": row[2]} for row in cursor.fetchall()]
    conn.close()
    return articles

@app.get("/")
def home():
    return {"message": "Vítejte v News API! Použijte /articles pro získání novinek."}

@app.get("/articles")
def read_articles(source: str = Query(None, description="Filtrujte podle zdroje (např. idnes.cz)")):
    return get_articles(source)