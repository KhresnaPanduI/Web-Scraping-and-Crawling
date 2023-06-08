import traceback
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests, os

BASE_PATH = r"C:\Users\Aevum\Documents\Telkom\Crawler\Documents"

def crawl():
    url_perda = 'https://jdih.musirawaskab.go.id/halkatprodukhukum-46-1.html'
    url_perbup = 'https://jdih.musirawaskab.go.id/kategoriprodukhukum-41-peraturan-bupati.html'
    main_url = "https://jdih.musirawaskab.go.id/haldownload-1.html"

    # Send a GET request to the URL and fetch the HTML content
    response = requests.get(main_url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    '''
    # Find all the <a> tags with the specified tag name and extract the text and href
    results = soup.find_all('span', class_='in-header')

    # Extract the text value and href for each matching element
    text_values = [result.a.text for result in results]
    href_values = [urljoin(url_perda, result.a['href']) for result in results]

    # Print the extracted values
    print("Text Values:", text_values)
    print("Href Values:", href_values)

    res = requests.get(href_values[0])
    '''

    # Find all table rows except the header
    rows = soup.select('table tr')[1:]

    # Find the last page link
    last_page_link = soup.select('.pagenation li a')[-1]

    # Extract the value of the last page
    last_page = int(last_page_link.text.strip())

    print("Last page: ", last_page)

    # Iterate over each row and extract document names and download links
    i = 1
    for row in rows:
        print("No: ", i)
        if i == 10:
            break

        # Extract document name
        nama_dokumen = row.select_one('.nama_pengajar').text

        # Extract download link
        link_download = row.select_one('.read-more2')['href']

        # Determine the destination directory based on the document name
        if 'peraturan daerah' in nama_dokumen.lower():
            dest_directory = os.path.join(BASE_PATH, 'PERATURAN DAERAH')
        elif 'peraturan bupati' in nama_dokumen.lower():
            dest_directory = os.path.join(BASE_PATH, 'PERATURAN BUPATI')
        else:
            continue  # Skip saving the file if it doesn't match the conditions

        # Create the full file path
        file_path = os.path.join(dest_directory, f'{nama_dokumen}.pdf')

        # Download the file
        response = requests.get(urljoin(main_url, link_download))
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"File '{nama_dokumen}.pdf' downloaded successfully.")
        i += 1

    print("All files have been downloaded.")

crawl()