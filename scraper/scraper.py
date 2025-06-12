import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fetch_latest_game_info():
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with open('config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(config['summoner_url'])
    time.sleep(30)

    try:
        consent_button = driver.find_element(By.XPATH, "//button[contains(., 'Consent')]")
        consent_button.click()
        time.sleep(30)
    except Exception:
        pass

    try:
        update_button = driver.find_element(By.XPATH, "//button[contains(., 'Updated')]")
        update_button.click()
        time.sleep(30)
    except Exception:
        pass

    try:
        kda_element = driver.find_element(By.XPATH, ".//p[span[@class='death']]")
        kda_spans = kda_element.find_elements(By.TAG_NAME, "span")
        k = kda_spans[0].text if len(kda_spans) > 0 else ""
        d = kda_spans[2].text if len(kda_spans) > 2 else ""
        a = kda_spans[4].text if len(kda_spans) > 4 else ""

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
