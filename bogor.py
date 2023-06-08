import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random, time, datetime, traceback, os, requests

BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\ChromeDriver 112.0.5615.49\chromedriver.exe")

wait = WebDriverWait(driver, 10)
dic = {'Peraturan Wali kota':'PERATURAN BUPATI', 'Peraturan Daerah':'PERATURAN DAERAH'}

def crawl():
    try:
        time.sleep(2)
        for key, value in dic.items():
            url = "https://jdih.kotabogor.go.id/"
            driver.get(url)
            time.sleep(2)
            perda_button = driver.find_element(By.XPATH, "//h5[contains(text(), '{}')]/ancestor::button".format(key))
            time.sleep(2)
            perda_button.send_keys(Keys.RETURN)
            time.sleep(2)

            # Find all the card elements
            cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'accordion-group')]/div[@class='card']")

            # Iterate through each card and extract the text value and href
            i = 1
            for card in cards:
                if i == 4:
                    break
                # Extract the text value
                nama_file = card.find_element(By.XPATH, ".//button").text.strip()

                # Extract the href attribute
                href = card.find_element(By.XPATH, ".//a[contains(text(), 'Download File')]").get_attribute("href")

                print("Link untuk {}: {}".format(nama_file, href))
                file_name = str(nama_file) + ".pdf"
                path = BASE_PATH + "\{}".format(value)
                save_dir = os.path.join(path, file_name)

                response = requests.get(href, verify=False)
                with open(save_dir, 'wb') as f:
                    f.write(response.content)
                i += 1
        driver.quit()
    except:
        print('masuk exception')
        print(traceback.format_exc())
        driver.quit()
crawl()
