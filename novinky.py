from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.novinky.cz/sekce/domaci-13"

def chrom_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def handle_consent(driver):
    try:
        # Počkej max. 10 sekund, zda jsme přesměrováni na seznam.cz pro souhlas
        WebDriverWait(driver, 10).until(EC.url_contains("cmp.seznam.cz"))

        # Najdi a klikni na tlačítko "Souhlasím"
        souhlas_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                "div > div > div.dialog-intro.dialog-scrollable > div > ul > li.lg-min\\:d-grid.g-md.gtr-subgrid.gr-span-5.md-max\\:o-1 > div > button"))
        )
        driver.execute_script("arguments[0].click();", souhlas_button)
        print("Kliknuto na tlačítko 'Souhlasím'.")

        # Počkej na přesměrování na novinky.cz
        WebDriverWait(driver, 10).until(EC.url_contains("novinky.cz"))
        print("Přesměrování dokončeno.")

    except Exception as e:
        print("Tlačítko 'Souhlasím' nebylo nalezeno nebo nešlo kliknout.", e)

def find_articles(driver):
    try:
        driver.get(URL)  # Otevři hlavní stránku
        handle_consent(driver)  # Ošetření souhlasu

        # Počkej na načtení prvního článku
        article = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.mol-articles-container article"))
        ).text
        print("Nalezený článek:", article)

    except Exception as e:
        print("Články nebyly nalezeny:", e)

if __name__ == "__main__":
    driver = chrom_driver()
    find_articles(driver)
    driver.quit()
