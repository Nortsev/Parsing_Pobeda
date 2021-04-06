# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
link = ["https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/telefony/sotovye-telefony/?k=false&q=20&s=high&c=57&cg=143&a=0&f[]=400&",
            "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/?k=false&q=20&s=high&c=57&cg=99&a=0&f[]=400&",
            "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?k=false&q=20&s=high&c=57&cg=84&a=0&f[]=400&"
    ]
HEADERS  = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

product = []

def get_html(url, params=None):
    r = requests.get(url,headers = HEADERS, params=params)
    return r


def get_content (html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", attrs={"am-card-info":True})


    for item in items:
        product.append({
            'title': item.find('a',attrs={"am-card-title":True}).get_text(strip=True),
            'price': str(item.find('div',attrs={"am-card-prices":True}).get_text(strip=True)).partition("a")[0]+" руб"
            })
    print(product)


def parse ():
    html = get_html(random.choice(link))
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Error conect")


parse()