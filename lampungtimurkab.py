import os, traceback
import requests, math, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

def crawl():
    try:
        url = r"http://jdih.lampungtimurkab.go.id/dokumen/peraturan?page=1&per-page=5"
        main_url = r"http://jdih.lampungtimurkab.go.id/"
        # Step 1: Parse the HTML content
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # find the last page
        last_page_text = soup.find('div', class_='list-view', id='w0').text.strip()
        pattern = r"Ditampilkan \d+ - \d+ dari (\d+) Data"

        matches = re.search(pattern, last_page_text)
        if matches:
            jumlah_dokumen = matches.group(1)
        last_page = math.ceil(int(jumlah_dokumen) / 5)
        print("Last Page: ", last_page)

        for i in range(1, last_page):
            if i == 5:
                break
            url_loop = r"http://jdih.lampungtimurkab.go.id/dokumen/peraturan?page={}&per-page=5".format(i)

            # Step 1: Parse the HTML content
            response = requests.get(url_loop)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Step 2: Find all div elements with class="item"
            divs = soup.find_all('div', class_='item')

            # Step 3-9: Iterate over each div element
            for div in divs:
                try:
                    # Step 4: Get the text value of <a> element with class="text-primary" and title="lihat detail"
                    nama_dokumen = div.find('a', class_='text-primary', title='lihat detail').text.strip()

                    # Step 5: Get the value of href attribute from the <a> element with title="lihat file", target="_blank", and text value "Dokumen"
                    download_link = div.find('a', href=True, title='lihat file', target='_blank', text='Dokumen')['href']

                    # Step 6: Join the main URL with the download link
                    combined_link = urljoin(main_url, download_link)

                    # Step 7: Download the file using requests.get()
                    response = requests.get(combined_link)

                    # Step 8: Replace escape characters or invalid characters in the file name with underscores
                    escaped_nama_dokumen = re.sub(r'[\\/:"*?<>|]', '_', nama_dokumen)
                    cut_name = escaped_nama_dokumen.split('TENTANG')[0] + 'TENTANG'
                    # Step 8: Save the file to a specific directory based on the document type
                    lowercase_nama_dokumen = cut_name.lower()

                    if 'peraturan daerah' in lowercase_nama_dokumen:
                        file_path = os.path.join(BASE_PATH, 'PERATURAN DAERAH', f'{cut_name}.pdf')
                    elif 'peraturan bupati' in lowercase_nama_dokumen:
                        file_path = os.path.join(BASE_PATH, 'PERATURAN BUPATI', f'{cut_name}.pdf')
                    else:
                        continue  # Skip saving the file for other cases and move to the next div

                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                    # Step 9: Print success message after successfully downloading each file
                    print(f"Successfully downloaded {cut_name}")
                except:
                    print('masuk exception')
                    print(traceback.format_exc())
    except:
        print('masuk exception')
        print(traceback.format_exc())

crawl()