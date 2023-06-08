from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import random
import time, traceback, glob, os, urllib.request
import datetime

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\chromedriver.exe")

# set download path
BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

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

def get_latest_file_download(download_dir):
    """
    Returns the latest file downloaded in the given directory
    """
    list_of_files = glob.glob(download_dir + '/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def crawl():
    try:
        url = "https://jdih.blorakab.go.id/"
        driver.get(url)
        wait = WebDriverWait(driver, 60)

        list_kategori = ['peraturan-daerah', 'peraturan-bupati', 'peraturan-desa']

        url = "https://jdih.blorakab.go.id/category/peraturan-daerah"
        driver.get(url)
        time.sleep(2)

        list_kategori = ['peraturan-daerah', 'peraturan-bupati', 'peraturan-desa']

        url = "https://jdih.blorakab.go.id/category/peraturan-daerah"
        driver.get(url)
        time.sleep(2)
        page = 1
        while True:
            print('Lagi di page   '
                  '-', page)
            page += 1
            time.sleep(2)
            # Click the next button if it exists
            next_buttons = driver.find_elements(By.XPATH, '//*[@id="DataTables_Table_0_next"]/a')
            next_button = next_buttons[0]

            # Check if the next button clickable
            next_buttons2 = driver.find_elements(By.XPATH, '//*[@id="DataTables_Table_0_next"]')
            next_button2 = next_buttons2[0]

            next_button2_class = next_button2.get_attribute('class')
            if 'disabled' not in next_button2_class:
                next_button.send_keys(Keys.RETURN)
            else:
                print('masuk break')
                break

        '''
        after_cari_handle = driver.current_window_handle
        # Wait for the table to be visible
        table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "DataTables_Table_0")))

        # Get all the rows in the table
        table_rows = table.find_elements(By.XPATH, ".//tbody/tr")

        print('number of row', len(table_rows))
        for row in table_rows:
            # Click the "Lihat / Unduh" link to download the file
            num_files = len(os.listdir(BASE_PATH))
            download_presence = EC.visibility_of_element_located((By.XPATH, './/a[contains(text(),"Lihat / Unduh")]'))
            time.sleep(1)
            download_link = row.find_element(By.XPATH, './/a[contains(text(),"Lihat / Unduh")]')
            print('Download link: ', download_link)
            download_link.send_keys(Keys.RETURN)

            # check if there is new file. If not continue to next row
            time.sleep(1)
            new_num_files = len(os.listdir(BASE_PATH))
            if new_num_files == num_files:
                print("Gagal download buat file: ", row.find_element(By.XPATH, './td[1]').text.strip())
                continue

            # wait until download complete
            download_time = download_wait(BASE_PATH)
            print("Time to download: {}s".format(download_time))

            # rename the file
            prev_name = get_latest_file_download(BASE_PATH)
            new_name = row.find_element(By.XPATH, './td[1]').text.strip()
            new_name = new_name + '.pdf'

            downloaded_file_path = get_latest_file_download(BASE_PATH)
            os.rename(downloaded_file_path, os.path.join(BASE_PATH, new_name))
            print('Previous name: {} New name: {}'.format(prev_name, new_name))

            # close the new tab and get back to after cari handle
            print('SWITCH TO LAST TAB')
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1)
            driver.close()
            driver.switch_to.window(after_cari_handle)
        '''
        driver.quit()

    except:
        print('masuk exception')
        print(traceback.format_exc())
        driver.quit()

crawl()