# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random

link = [
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/telefony/sotovye-telefony/?k=false&q=20&s=high&c=57&cg=143&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/?k=false&q=20&s=high&c=57&cg=99&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?k=false&q=20&s=high&c=57&cg=84&a=0&f[]=400&"
]
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

TOP_ITEMS = 5
DOMAIN = "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/"


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", attrs={"am-card-info": True})
    products = []
    for i in range(TOP_ITEMS):
        title = items[i].find('meta', attrs={"itemprop": "name"})['content'],
        price = items[i].find('span', attrs={"am-card-price": True})["content"],
        url = items[i].find('a', attrs={"am-card-title": True})['href']

        url_photo = DOMAIN + \
                    BeautifulSoup(get_html(url).text, "html.parser").find('img', attrs={"am-image-item": True})[
                        'am-original']
        photo = requests.get(url_photo).content
        products.append({"title": title[0],
                         "price": price[0],
                         "url": url,
                         "url_photo": url_photo,
                         "photo": photo
                         })

    return products

def save_img(products):
    for i in range(len(products)):

        with open(f'img/photo_{i}.jpg','wb') as f:

            f.write(products[i]["photo"])


def main():
    html = get_html(random.choice(link))
    if html.status_code != 200:
        print("Error conect")

    products = get_content(html.text)
    save_img(products)





main()
