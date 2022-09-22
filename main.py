import requests
from bs4 import BeautifulSoup
from Wikidb import wikiDB
import threading
from Creater import Creater
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

URLS = ['https://en.wikipedia.org/wiki/School']
EROR_URLS = []
Watching_urls = []
DOMEN = "https://en.wikipedia.org/"

db = Creater()


def get_html(url):
    html = requests.get(url, headers=HEADERS)
    return html


def get_urls_from_page(html, Url,DB):
    soup = BeautifulSoup(html, "lxml")
    toc = soup.find('div', class_='toc')
    P = toc.find_previous_siblings('p')
    url_ans = []

    for i in P:
        urls = i.find_all('a')
        for url in urls:
            href = url.get('href')
            if len(href.split('/')) > 1:

                if href.split('/')[1] == 'wiki':

                    k = DB.add_url(DOMEN + href, Url)

                    if k == 0:
                        url_ans.append(DOMEN + href)
                    id = DB.find_url(DOMEN + href)
                    DB.creat_mig(id, Url)

    return url_ans


def working_page(URL, k):
    DB = wikiDB()
    url = URL
    if url == -1:
        return 0
    try:
        html = get_html(url)
        if html.status_code == 200:
            DB.add_raw_urls(get_urls_from_page(html.text, url, DB))
        else:
            EROR_URLS.append(url)

    except:
        EROR_URLS.append(url)
        return 0


working_page("https://en.wikipedia.org/wiki/School", 1)

while True:
    url= db.get_raw_url()
    t1 = threading.Thread(target=working_page, args=(url[0], 1))
    t2 = threading.Thread(target=working_page, args=(url[1], 1))
    t3 = threading.Thread(target=working_page, args=(url[2], 1))
    t4 = threading.Thread(target=working_page, args=(url[3], 1))
    t5 = threading.Thread(target=working_page, args=(url[4], 1))
    t6 = threading.Thread(target=working_page, args=(url[5], 1))
    t7 = threading.Thread(target=working_page, args=(url[6], 1))
    t8 = threading.Thread(target=working_page, args=(url[7], 1))
    t9 = threading.Thread(target=working_page, args=(url[8], 1))
    t10 = threading.Thread(target=working_page, args=(url[9], 1))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
