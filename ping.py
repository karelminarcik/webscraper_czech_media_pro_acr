import requests
import time

URL = "https://webscraper-czech-media.onrender.com"

while True:
    try:
        response = requests.get(URL)
        print(f"Ping: {response.status_code}")
    except requests.RequestException as e:
        print(f"Chyba při pingování: {e}")
    
    time.sleep(600)  # Počkáme 10 minut a znovu pingneme
