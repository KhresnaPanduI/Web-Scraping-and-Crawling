from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
import time, traceback, datetime, random, os, requests

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\chromedriver.exe")

PATH_PERDA = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents\PERATURAN DAERAH"
PATH_PERBUP = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents\PERATURAN BUPATI"

def download_wait(path_to_downloads):
    timeout = 0
    dl_wait = True
    # wait for maximum 5 minutes
    while dl_wait and timeout < 300:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        timeout += 1
    return timeout

def crawler():
    url = "https://jdihnew.jepara.go.id/"
    driver.get(url)

    # Get the current window tab (https://jdihnew.jepara.go.id/) to switch back later
    main_window_handle = driver.current_window_handle

    last_page_button = driver.find_element(By.CSS_SELECTOR, 'a.page-link[aria-controls="table1"][data-dt-idx="7"]')
    last_page = int(last_page_button.text)
    print("last page: ", last_page)

    curr_page = 1
    while curr_page < last_page:
        if curr_page == 3:
            break
        print("Lagi di page: ", curr_page)
        time.sleep(5)
        # Wait for the table to be present
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "table1"))
        )
        tbody = table.find_element(By.CSS_SELECTOR, 'tbody')
        # Find all the rows in the table

        rows = tbody.find_elements(By.CSS_SELECTOR, 'tr[role="row"]')
        for row in rows:
            # try except block for each document
            try:
                cells = row.find_elements(By.CSS_SELECTOR, 'td')
                tahun = cells[1].text
                nomor = cells[2].text
                kategori = cells[3].text

                # Wait for the download button to be clickable
                download_button = WebDriverWait(row, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-sm.btn-success[title='Unduh']"))
                )

                # extract element value
                download_url = download_button.get_attribute("href")

                filename = f"{kategori} Nomor {nomor} Tahun {tahun}.pdf"
                # save file according to the category
                if kategori == "PERATURAN DAERAH":
                    filepath = os.path.join(PATH_PERDA, filename)
                elif kategori == "PERATURAN BUPATI":
                    filepath = os.path.join(PATH_PERBUP, filename)
                else: # if neither, do not need to download
                    continue

                response = requests.get(download_url)
                with open(filepath, "wb") as f:
                    f.write(response.content)

                # Wait for the file to download
                print('Downloaded: {}'.format(filename))
            except:
                print("Gagal download")

        time.sleep(1)
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#table1_next > a'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.send_keys(Keys.RETURN)
        # the error above is very common to happen randomly
        # we will wait and retry to click the next button
        except StaleElementReferenceException or ElementNotInteractableException:
            time.sleep(5)
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#table1_next > a'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.send_keys(Keys.RETURN)

        curr_page += 1

    time.sleep(1)


    driver.quit()

crawler()

