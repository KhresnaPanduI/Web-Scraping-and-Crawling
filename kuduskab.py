import time
from bs4 import BeautifulSoup
import requests
from lxml import html

# URL of the web page
url = "https://jdih.kuduskab.go.id/himpunan_perundangan?kategori=8"

# Make a GET request to the web page
response = requests.get(url)

# Parse the HTML content using lxml
tree = html.fromstring(response.content)

# Extract the download URL using XPath
'''
download_url = tree.xpath("//div[@class='btn btn-default']/a[@target='_blank']/@href")

print(download_url)
# Make a GET request to the download URL
# Save the file to disk
i = 1
for url in download_url:
    time.sleep(2)
    response = requests.get(url)
    with open("file ke-{}.pdf".format(i), "wb") as f:
        f.write(response.content)
    i += 1
'''
url = "https://jdih.kuduskab.go.id/himpunan_perundangan?kategori=8"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

links = soup.find_all("a")
i = 0
for link in links:
    if "download" in link["href"]:
        print(link)
        download_url = "https://jdih.kuduskab.go.id/himpunan_perundangan/" + link["href"]
        r = requests.get(download_url, allow_redirects=True)
        open(link.text, 'wb').write(r.content)