from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random, time, traceback, os
import datetime

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\chromedriver.exe")

def download_wait(
        path_to_downloads):
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

def crawl():
    try:
        url = "http://jdih.garutkab.go.id/"
        driver.get(url)

        # Get the current window tab ("https://jdih.cirebonkab.go.id/) to switch back later
        main_window_handle = driver.current_window_handle
        time.sleep(1)
        driver.maximize_window()

        # Wait until navbar loaded
        wait = WebDriverWait(driver, 60)
        navbar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]')))

        # list of all kategori
        list_kategori = ['peraturan-daerah', 'peraturan-bupati', 'keputusan-bupati', 'peraturan-desa']
        # get all the link elements and store them in a list

        for kategori in list_kategori:
            # select peraturan daerah in di navbar
            driver.execute_script("window.open('http://jdih.garutkab.go.id/produk/{}', 'new tab')".format(kategori))
            # switch to the kategori tab
            driver.switch_to.window(driver.window_handles[-1])

            # wait until the navbar loaded
            navbar_download = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="product-daerah-list"]//a[2]')))
            time.sleep(5)
            # get the last pages
            pages = int(driver.find_element(By.XPATH, '//*[@id="main"]/section[2]/div/div[3]/div/nav/ul/li[last()-1]/a')
                        .get_attribute("textContent"))

            print('Number of pages: ', pages)

            # iterate until last page
            for i in range(pages - 1):
                print('In page-{} of {}'.format(i+1, kategori))
                # Find the "next" button and wait until element is clickable
                next_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']")))
                time.sleep(2)
                # scroll to the button
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(2)
                # Click the "next" button
                print('otw click')
                next_button.click()
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    f"//*[@id='main']/section[2]/div/div[3]/div/nav/ul/li[@class='page-item active']/a[text()='{i + 2}']")))
                time.sleep(2)
                print('setelah click')

                link_elements = driver.find_elements(By.XPATH, '//*[@id="product-daerah-list"]//a[2]')
                for link in link_elements:
                    driver.execute_script("window.open(arguments[0], '_blank')", link.get_attribute("href"))
                    time.sleep(1)
            time.sleep(2)
            driver.close()
            driver.switch_to.window(main_window_handle)



        driver.quit()
        # comment block start here
        # iterate through ['Peraturan Daerah', 'Peraturan Bupati', 'Keputusan Bupati',
        # 'Peraturan Desa', 'Undang-undang']
        # comment block end here
    except:
        print('masuk exception')
        print(traceback.format_exc())
        driver.quit()

crawl()