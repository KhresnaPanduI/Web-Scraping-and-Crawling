import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re, os, traceback

# Define the base path for saving the downloaded files
BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

def crawl():
    try:
        # Step 1: Get the HTML content of the main page
        main_url = "https://jdih.lubuklinggaukota.go.id/document/index/15/15"
        response = requests.get(main_url)
        html_content = response.content

        # Step 2: Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        pagination_div = soup.find('div', class_='pagination')
        a_tag = pagination_div.find_all('a')[-1]
        last_page = int(a_tag['data-ci-pagination-page'])

        print("Last Page: ", last_page)
        page = 15
        for i in range(1, last_page):
            print("Lagi di page: ", i)
            url = "https://jdih.lubuklinggaukota.go.id/document/index/15/{}".format(page)
            response = requests.get(url)
            html_content = response.content

            # Step 2: Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Step 3: Find all div elements with class="col-md-12"
            document_divs = soup.find_all('div', class_='col-md-12')
            # Step 4-13: Iterate over each document div and extract the necessary information
            for div in document_divs:
                try:
                    # Step 4: Get the href value of the detailed page
                    detailed_page = div.find('a')['href']
                    print("Detailed page: ", detailed_page)
                    # Step 5: Open the detailed page using requests.get
                    detailed_response = requests.get(detailed_page)
                    detailed_soup = BeautifulSoup(detailed_response.content, 'html.parser')

                    # Step 6: Extract the download link from the detailed page
                    download_link = detailed_soup.find('div', class_='col-lg-4').find('object')['data']
                    download_link = quote(download_link, safe=':/')
                    print("Download link: ", download_link)

                    # Extract the text value of <b>PERATURAN DAERAH KOTA</b> and store it in 'jenis'
                    jenis = detailed_soup.find('dt', string='singkatan jenis / bentuk peraturan').find_next_sibling('dd').text.strip()
                    # Extract the text value of <dt>Nomor Peraturan</dt> and store it in 'nomor'
                    nomor = detailed_soup.find('dt', string='Nomor Peraturan').find_next_sibling('dd').text.strip()
                    # Extract the text value of <dt>Tahun Terbit</dt> and store it in 'tahun'
                    tahun = detailed_soup.find('dt', string='Tahun Terbit').find_next_sibling('dd').text.strip()

                    # Step 7: Download the document using requests.get
                    document_response = requests.get(download_link)

                    # Step 8-13: Save the document to the specified path based on conditions
                    nama_dokumen = "{} Nomor {} Tahun {}.pdf".format(jenis, nomor, tahun)

                    if 'perda' in nama_dokumen.lower():
                        save_path = os.path.join(BASE_PATH, "PERATURAN DAERAH", nama_dokumen)
                    elif 'perwal' in nama_dokumen.lower():
                        save_path = os.path.join(BASE_PATH, "PERATURAN BUPATI", nama_dokumen)
                    else:
                        continue

                    with open(save_path, 'wb') as file:
                        file.write(document_response.content)
                    print(f"Successfully downloaded {nama_dokumen}")
                except:
                    print('masuk exception')
                    print(traceback.format_exc())
            page += 15
    except:
        print('masuk exception')
        print(traceback.format_exc())

crawl()