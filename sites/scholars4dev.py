from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import hashlib


def parse_site(links):
    url = 'http://www.scholars4dev.com/category/level-of-study/undergraduate-scholarships/'

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()

    soup = BeautifulSoup(web_byte, "html.parser")
    parent = soup.find('div', class_='maincontent')

    inner_items = [article for article in parent.find_all('a', href=True)]

    for i in range(0, len(inner_items)):
        text = inner_items[i].text
        href = inner_items[i]['href']

        if len(text) > 5 and text != 'Last »' and text != '»' and text != 'Why subscribe?' and text != 'Read More':
            links.append({
                "heading": text,
                "href": href,
                "cache": hashlib.sha256(
                    text.encode('utf-8') + href.encode('utf-8')).hexdigest()
            })
