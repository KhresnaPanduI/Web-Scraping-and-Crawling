from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time, traceback, glob, os, urllib.request, random, requests
import datetime

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\ChromeDriver 112.0.5615.49\chromedriver.exe")
wait = WebDriverWait(driver, 60)

# set download path
BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

def crawl():
    try:
        url = "https://jdih.karimunkab.go.id/unduh"
        driver.get(url)


        # Step 2: Find the table body on the main page
        table_body = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mytable1")))
        i = 1
        while True:
            print("Lagi di page: ", i)
            i += 1
            if i == 4:
                break
            # Step 3: Get all the table rows on the main page
            rows = table_body.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                time.sleep(2)
                # Step 4: Get the link to the detailed page
                links = row.find_elements(By.CSS_SELECTOR, "#mytable1 > tbody > tr > td:nth-child(4) > center > a")
                for link in links:
                    try:
                        download_link = link.get_attribute("href")
                        # Step 5: Open the detailed page with Beautiful Soup
                        detailed_page_response = requests.get(download_link)
                        detailed_page_soup = BeautifulSoup(detailed_page_response.content, "html.parser")

                        # Step 6: Find the table on the detailed page
                        detailed_table = detailed_page_soup.find("table", class_="table-sm")

                        # Step 7: Extract the value of the third td in the third row
                        jenis_dokumen = detailed_table.find_all("tr")[2].find_all("td")[2].text

                        # Step 8: Extract the value of the third td in the fifth row
                        nomor = detailed_table.find_all("tr")[4].find_all("td")[2].text

                        # Step 8: Extract the value of the third td in the sixth row
                        tahun = detailed_table.find_all("tr")[5].find_all("td")[2].text

                        # Step 9: Find the download button and get the download link
                        download_button = detailed_page_soup.find('button', {'class': 'btn btn-primary btn-sm', 'type': 'submit'})
                        download_link = download_button.parent['href']
                        print("Download link: ", download_link)
                        # Step 10: Create the file name
                        nama_file = f"{jenis_dokumen} Nomor {nomor} Tahun {tahun}.pdf"
                        lowercase_nama_file = nama_file.lower()
                        if 'peraturan daerah' in lowercase_nama_file:
                            save_path = os.path.join(BASE_PATH, "PERATURAN DAERAH", nama_file)
                            # download_file(nama_file, download_link, save_path)
                        elif 'peraturan bupati' in lowercase_nama_file:
                            save_path = os.path.join(BASE_PATH, "PERATURAN BUPATI", nama_file)
                            # download_file(nama_file, download_link, save_path)
                        else:
                            print(f"Not saving {nama_file} because it's not peraturan daerah or peraturan bupati")
                        # Step 11: Download the file using requests.get
                        file_response = requests.get(download_link)
                        with open(save_path, "wb") as file:
                            file.write(file_response.content)

                        # Step 12: Print a success message
                        print(f"Successfully downloaded {nama_file}")

                        # Delay before iterating to the next row
                        time.sleep(1)
                    except:
                        print('masuk exception')
                        print(traceback.format_exc())

            # Step 4-11: Loop through each row and perform the required steps
            # Click the next button if it exists
            #next_buttons = driver.find_elements(By.XPATH, '//*[@id="mytable1_next"]a')
            #next_button = next_buttons[0]

            # Check if the next button clickable
            next_buttons2 = driver.find_elements(By.XPATH, '//*[@id="mytable1_next"]')
            next_button2 = next_buttons2[0]

            next_button2_class = next_button2.get_attribute('class')
            if 'disabled' not in next_button2_class:
                next_button2.send_keys(Keys.RETURN)
                #table_body = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mytable1")))
            else:
                print('Page terakhir selesai')
                break
        driver.quit()
    except:
        print('masuk exception')
        print(traceback.format_exc())
        driver.quit()

crawl()