import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random, time, datetime, traceback, os

BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\ChromeDriver 112.0.5615.49\chromedriver.exe")

wait = WebDriverWait(driver, 10)
dic = {"PERATURAN DAERAH":11, "PERATURAN BUPATI":12}
list_uu = ['https://jdih.bekasikab.go.id/index.php/page/produk_hukum/11/', 'https://jdih.bekasikab.go.id/index.php/page/produk_hukum/12/']
def crawl():
    try:
        for key, value in dic.items():
            print("Crawling ", key)
            url = "https://jdih.bekasikab.go.id/index.php/page/produk_hukum/{}/".format(value)
            driver.get(url)

            # Get the current window tab ("https://jdih.kemendag.go.id") to switch back later
            main_window_handle = driver.current_window_handle

            # loop through all the pages
            page = 1

            # Find the element and get its text value
            element = driver.find_element(By.XPATH,
                "//a[@class='page-link' and @data-dt-idx='7']")
            last_page = element.text
            """
            for i in range(page, int(last_page)):
                print('Lagi di page: ', i)
                time.sleep(1)
                # wait for the link to be clickable
                link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#table_idku_next > a")))
                time.sleep(1)
                # click the link
                link.send_keys(Keys.RETURN)
            """

            # Get the table element
            table = driver.find_element(By.ID, "table_idku")

            # Get the tbody element
            tbody = table.find_element(By.TAG_NAME, "tbody")

            # Iterate through every row in the table
            data = []
            for row in tbody.find_elements (By.TAG_NAME, "tr"):
                # Extract the value of the first column
                no_uu = row.find_element(By.XPATH, ".//td[1]").text

                # Extract the href attribute of the fourth column
                doc_link = row.find_element(By.XPATH, ".//td[4]/a").get_attribute("href")
                print("Link untuk {}: {}".format(no_uu, doc_link))
                file_name = str(no_uu) + ".pdf"
                path = BASE_PATH + "\PERATURAN BUPATI"
                save_dir = os.path.join(path, file_name)

                # get the download link
                response = requests.get(doc_link)
                soup = BeautifulSoup(response.content, 'html.parser')
                res = soup.find('a', {'class': 'btn btn-primary'})
                download_link = res.get('href')

                # download the file
                response = requests.get(download_link)
                with open(save_dir, 'wb') as file:
                    file.write(response.content)

                print("Succesully download: ", file_name)
        time.sleep(2)

        driver.quit()
    except Exception as e:
        print('masuk exception')
        print(traceback.format_exc())
        driver.quit()

crawl()