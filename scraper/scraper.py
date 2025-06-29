import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth # Import selenium-stealth

def fetch_latest_game_info():
    options = Options()
    options.add_argument("--mute-audio")
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    with open('config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(config['summoner_url'])

    time.sleep(10)

    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consent')]"))
        )
        consent_button.click()
        time.sleep(5)
    except Exception:
        pass

    try:
        update_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Updated')]"))
        )
        update_button.click()
        time.sleep(5)
    except Exception:
        pass

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, ".//p[span[@class='death']]"))
        )
    except Exception as e:
        driver.quit()
        return None, None, None, None, None

    try:
        kda_element = driver.find_element(By.XPATH, ".//p[span[@class='death']]")
        kda_spans = kda_element.find_elements(By.TAG_NAME, "span")
        k = kda_spans[0].text if len(kda_spans) > 0 else "0"
        d = kda_spans[2].text if len(kda_spans) > 2 else "0"
        a = kda_spans[4].text if len(kda_spans) > 4 else "0"

        ai_score_element = driver.find_element(By.XPATH, "//h5[normalize-space(.)='AI-Score']/following::span[1]")
        ai_score = ai_score_element.text

        dt_home = driver.find_element(By.CSS_SELECTOR, "dt.home")
        champ_img = dt_home.find_element(By.XPATH, ".//img[contains(@src, '/champion/')]")
        champion_name = champ_img.get_attribute("alt")

        result_element = driver.find_element(By.XPATH, "//span[normalize-space(text())='Win' or normalize-space(text())='Lose']")
        result = result_element.text

        game_id = f"{k}/{d}/{a}|{ai_score}"

        driver.quit()
        return game_id, ai_score, champion_name, f"{k}/{d}/{a}", result

    except Exception as e:
        print(f"Error parsing game: {e}")
        driver.quit()
        return None, None, None, None, None