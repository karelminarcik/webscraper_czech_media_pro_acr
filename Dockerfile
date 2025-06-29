# Použij oficiální Python image
FROM python:3.11-slim

# Nastav pracovní adresář v kontejneru
WORKDIR /app

# Zkopíruj requirements.txt a nainstaluj závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj zbytek projektu do kontejneru
COPY . .

# Ujisti se, že news.db nebude přepisována při buildu (volitelné)
# Pokud chceš čistou DB při každém buildu, tento řádek vynech

# Otevři port 8000 pro FastAPI
EXPOSE 8000

# Spusť FastAPI server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
