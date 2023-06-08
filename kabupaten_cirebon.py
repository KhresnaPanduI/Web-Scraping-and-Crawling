from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import time, traceback
import datetime

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r"C:\Users\Aevum\Documents\Telkom\chromedriver.exe")

def crawl():
    try:
        url = "https://jdih.cirebonkab.go.id/"
        driver.get(url)

        # Get the current window tab ("https://jdih.cirebonkab.go.id/) to switch back later
        main_window_handle = driver.current_window_handle

        time.sleep(1)
        # Wait for the presence of 'Semua Kategori' and 'Semua Tahun' text for maximum 60 seconds
        wait = WebDriverWait(driver, 60)
        kategorireg = wait.until(EC.presence_of_element_located((By.XPATH, '//option[text()="Semua Kategori"]')))
        tahunreg = wait.until(EC.presence_of_element_located((By.XPATH, '//option[text()="Semua Tahun"]')))
        time.sleep(3)

        # Get all tahun value
        tahun_dropdown = driver.find_elements(By.XPATH, '//select[@name="tahun"]/option[@value and @value!=""]')
        tahun_list = [tahun.text for tahun in tahun_dropdown]

        # Get all kategori value
        kategori_dropdown = driver.find_elements(By.XPATH, '//select[@name="jenis"]/option[@value and @value!=""]')
        kategori_list = [kategori.text for kategori in kategori_dropdown]

        print('kategori yang ada: ', kategori_list)

        # Exclude some value in kategori
        exclude = ['Undang-Undang Dasar 1945', 'Keputusan DPRD', 'Naskah Akademis']

        for kategori in kategori_list:
            if kategori in exclude:
                kategori_list.remove(kategori)

        print('tahun yang ada: ', tahun_list)
        print('kategori setelah dihapus: ', kategori_list)

        # start of comment block
        '''
        # Select tahun value
        tahun_dropdown = driver.find_element(By.NAME, 'tahun')
        tahun_select = Select(tahun_dropdown)
        tahun_select.select_by_value('2018')

        # Select kategori value
        kategori_dropdown = driver.find_element(By.NAME, 'jenis')
        kategori_select = Select(kategori_dropdown)
        kategori_select.select_by_value("Perda (Peraturan Daerah)")

        # Press Ctrl+Enter to submit the form and open the link in a new tab
        search_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-search-icon')
        search_button.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        # save the tab handle
        after_search_handle = driver.current_window_handle
        time.sleep(1)

        # wait for the pagination links to load
        print('LAGI NUNGGU')
        driver.implicitly_wait(10)
        # Find all the pagination elements excluding the 'previous' and 'next' buttons
        pagination_elements = driver.find_elements(By.XPATH,
            '//*[@id="example_paginate"]/ul/li[position()>1 and not(contains(@class, "previous") or contains(@class, "next"))]')

        # Count the number of pages
        page_count = len(pagination_elements)

        print(f'Total Number of Pages: {page_count}')

        # iterate over all the pages and click on each of them
        for i in range(2, page_count+2): # because the id of page 1 is 2
            print('Lagi di page {}'.format(i-1))
            driver.switch_to.window(after_search_handle)
            time.sleep(2)
            page_link = driver.find_element(By.XPATH, f'//*[@id="example_paginate"]/ul/li[{i}]/a')
            page_link.click()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])

            ### download all documents in the page
            # wait for the table to load
            # wait for the table to load
            rows = driver.find_elements(By.XPATH, "//tbody/tr")
            #rows = table.find_element(By.TAG_NAME, 'tr')
            print(rows)
            # iterate over all the rows in the table (excluding the header row)
            for row in rows[1:]:
                # get the link to the document
                link = row.find_element(By.XPATH, './td[5]/a')

                # download the document
                link.send_keys(Keys.CONTROL + Keys.RETURN)

                # wait for the download to complete
                time.sleep(5)

                # Switch to the new tab and close it
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
                driver.switch_to.window(after_search_handle)


        time.sleep(30)
        # End of comment block
        '''

        # iterate through all the year
        for tahun in tahun_list:
            # iterate through all the jenis dokumen
            for kategori in kategori_list:
                driver.switch_to.window(main_window_handle)

                print("Lagi di tahun = {}, dokumen = {}".format(tahun, kategori))

                # Select tahun value
                tahun_dropdown = driver.find_element(By.NAME, 'tahun')
                tahun_select = Select(tahun_dropdown)
                tahun_select.select_by_value(tahun)
                
                # Select kategori value
                kategori_dropdown = driver.find_element(By.NAME, 'jenis')
                kategori_select = Select(kategori_dropdown)
                kategori_select.select_by_value(kategori)

                # Press Ctrl+Enter to submit the form and open the link in a new tab
                search_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-search-icon')
                search_button.send_keys(Keys.CONTROL + Keys.RETURN)
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)

                # save the tab handle
                after_search_handle = driver.current_window_handle
                time.sleep(1)

                # wait for the pagination links to load
                driver.implicitly_wait(10)
                # Find all the pagination elements excluding the 'previous' and 'next' buttons
                pagination_elements = driver.find_elements(By.XPATH,
                                                           '//*[@id="example_paginate"]/ul/li[position()>1 and not(contains(@class, "previous") or contains(@class, "next"))]')

                # Count the number of pages
                page_count = len(pagination_elements)

                print(f'Total Number of Pages: {page_count}')

                # iterate over all the pages and click on each of them
                for i in range(2, page_count + 2):  # because the id of page 1 is 2
                    print('Lagi di page {}'.format(i - 1))
                    driver.switch_to.window(after_search_handle)
                    page_link = driver.find_element(By.XPATH, f'//*[@id="example_paginate"]/ul/li[{i}]/a')
                    page_link.click()
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[-1])

                    ### download all documents in the page
                    # wait for the table to load
                    # wait for the table to load
                    rows = driver.find_elements(By.XPATH, "//tbody/tr")
                    # rows = table.find_element(By.TAG_NAME, 'tr')
                    print(rows)
                    # iterate over all the rows in the table (excluding the header row)
                    for row in rows[1:]:
                        # get the link to the document
                        link = row.find_element(By.XPATH, './td[5]/a')

                        # download the document
                        link.send_keys(Keys.CONTROL + Keys.RETURN)

                        # wait for the download to complete
                        time.sleep(5)

                        # Switch to the new tab and close it
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        driver.switch_to.window(after_search_handle)

                # close the after search tab
                driver.close()
                driver.switch_to.window(main_window_handle)
        driver.quit()
    except Exception as e:
        print('masuk exception')
        print(traceback.format_exc())
        driver.quit()

crawl()