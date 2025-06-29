# 🧠 Czech News Web Scraper Project

This Python-based project regularly scrapes selected Czech news portals for relevant articles based on a defined list of keywords. Filtered articles are stored in a SQLite database and displayed to users via a responsive frontend web interface.

---

## ⚙️ Project Components

### 📂 Scrapers (`scrapers/`)
- Each file (e.g., `idnes_scraper.py`, `ct24.py`, `novinky_scraper.py`) contains a scraper specific to a news website.
- A scraper:
  - Loads the HTML page using `requests` and `BeautifulSoup`.
  - Extracts news articles.
  - Filters them using defined keywords (`common/keywords.py`).
  - Saves matching results into `news.db`.

### 🧩 `common/keywords.py`
- Stores the list of keywords used for article filtering.

### 📦 `api.py`
- Provides a REST API using **FastAPI**, acting as the backend interface to the SQLite database (`news.db`).
- Endpoints:
  - `/` – Root route returning a welcome message.
  - `/articles` – **GET** endpoint that returns articles, optionally filtered by `source`.
  - `/scrape` – **GET** endpoint that starts the scraping process in the background using `BackgroundTasks`. Ideal for cronjob scheduling.
  - `/articles` – **DELETE** endpoint to delete:
    - A specific article by `id`, or
    - All articles from a given `source`.

  If neither parameter is provided, a 400 Bad Request error is returned.

- ✨ CORS is enabled (currently `allow_origins=["*"]`, but can be restricted to domains such as `rentaacr.cz`).

### 🗃️ Database
- `news.db`: SQLite database storing all filtered articles.
- Scrapers insert new articles directly into this database.

---

## 🧪 Running & Deployment

### Scripts:
- `render-build.sh`: Build script used for deployment on [Render.com](https://render.com).
- `render.yaml`: Configuration file for Render deployment.
- External service [cronjob.com](https://cronjob.com) is used to trigger the scraper every 30 minutes.

---

## 🖼️ Frontend

- The web frontend:
  - Uses **JavaScript (fetch API)** to asynchronously retrieve articles from the REST endpoint at `https://webscraper-czech-media.onrender.com/articles`.
  - Articles are sorted by `date_added` and displayed dynamically in a table.
  - Each news source is color-coded using badges for better visual distinction.
  - Users can search articles in real-time or load more using a "Load More" button.
  - **Bootstrap** is used for responsive styling.

---

## 🔄 Workflow

1. A cronjob triggers `scraper.py` every 30 minutes.
2. The script iterates through all scraper modules and collects new articles.
3. Articles are filtered using keyword logic and saved into `news.db`.
4. The frontend (hosted on Vedos.cz) fetches data via the API and displays it.
5. Users see the latest articles in a clean, mobile-friendly interface.

---

## 🚀 Deployment Overview

- **Backend + scraping** runs on [Render.com](https://render.com).
- **Scraping scheduler** is managed via [cronjob.com](https://cronjob.com).
- **Frontend** is hosted separately on [Vedos.cz](https://www.vedos.cz/) and communicates with the API.

---

## 📌 Future Improvements (Suggestions)

- Add user authentication to protect admin routes (e.g., deletion).
- Switch from SQLite to PostgreSQL for production-scale deployments.
- Add unit tests for scraper and API logic.
- Add article image thumbnails.
- Improve keyword filtering using NLP techniques.

---

## 📬 Contact

For more information or contributions, visit: [https://www.rentaacr.cz](https://www.rentaacr.cz)
