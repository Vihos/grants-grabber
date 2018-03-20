import urllib.request
from bs4 import BeautifulSoup
import re
import hashlib


def parse_site(links):
    url = urllib.request.urlopen('http://st-gr.com/?cat=3')
    data = url.read()

    soup = BeautifulSoup(data, "html.parser")
    parent = soup.find('main', class_='site-main')

    inner_items = [article for article in parent.find_all('a', href=True)]

    p = re.compile('(.)*([0-9]{1,2}.[0-9]{1,2}.[0-9]{4}[0-9]{1,2}.[0-9]{1,2}.[0-9]{4})(.)*')
    p2 = re.compile('(.)*(Page)(.)*')

    for i in range(0, len(inner_items)):
        text = inner_items[i].text

        if text != "2017" and text != "2018" and text != "2019" and len(text) > 5 and not p.match(text) \
                and not p2.match(text):
            links.append({
                "heading": inner_items[i].text,
                "href": inner_items[i]['href'],
                "cache": hashlib.sha256(
                    inner_items[i].text.encode('utf-8') + inner_items[i]['href'].encode('utf-8')).hexdigest()
            })
