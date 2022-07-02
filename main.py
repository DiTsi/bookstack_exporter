import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://wiki.ditsi.ru"
download_path = os.path.realpath("./downloads")
prefs = {'download.default_directory' : download_path}

chrome_options = Options()

chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent={Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36}")
driver = webdriver.Chrome("/usr/bin/chromedriver", options=chrome_options)
driver.get(URL)

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
pager = soup.find("div", {"class": "grid third"})
books = pager.findAll("a", {"class": "grid-card"}, href=True)
books_links = []

for i in books:
    books_links.append(i['href'])

for book in books_links:
    driver.get(book)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    content = soup.find("div", {"class": "book-content"})
    articles_div = content.find("div", {"class": "entity-list book-contents"})
    if articles_div is None:
        continue
    articles = articles_div.findAll("a", {"class": "page entity-list-item"}, href=True)
    if len(articles) == 0:
        continue

    book_name = book.split('/')[-1]
    if not os.path.exists(download_path + '/' + book_name):
        os.mkdir(download_path + '/' + book_name)
    for article in articles:
        article_name = article['href'].split('/')[-1]
        url = article['href'] + '/export/markdown'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36', 'Referer': 'https://www.nseindia.com/'}
        r = requests.get(url, allow_redirects=True, headers=headers, verify=False)
        open(download_path + '/' + book_name + '/' + article_name, 'wb').write(r.content)

driver.close()
