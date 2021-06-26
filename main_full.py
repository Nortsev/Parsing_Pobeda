# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
from base_sqllite import SQLApi
from vk_api_pobeda import VKApi
import config
import re

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

TOP_ITEMS = 5
DOMAIN = "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/"


def get_html(url: str, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_content(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", attrs={"am-card": "normal"})
    products = []

    for item in items:
        if len(products) >= TOP_ITEMS:
            break

        # Continue if item does not have photo
        image_path = item.find("img", attrs={"itemprop": "image"})['src']
        title = item.find('meta', attrs={"itemprop": "name"})['content']
        if "noimage" in image_path or re.search(config.filter, title, re.IGNORECASE):
            continue



        price = item.find('span', attrs={"am-card-price": True})["content"]
        url = item.find('a', attrs={"am-card-title": True})['href']

        url_photo = DOMAIN + \
                    BeautifulSoup(get_html(url).text, "html.parser").find('img', attrs={"am-image-item": True})[
                        'am-original']
        photo = requests.get(url_photo).content
        products.append({"title": title,
                         "price": price,
                         "url": url,
                         "url_photo": url_photo,
                         "photo": photo
                         })

    return products


def main():
    # Initialize SQLApi
    sql_api = SQLApi()
    # Initialize VKApi
    vk_api = VKApi(config)
    html = get_html(random.choice(config.link))
    if html.status_code != 200:
        print("Error conect")

    web_products = get_content(html.text)
    sql_api.insert_products(web_products)
    products = sql_api.get_images()

    photos = [product['image'] for product in products]
    captions = [f"{product['title']} \n  Цена: {product['price']} \n Ссылка на товар на нашем сайте: {product['url']}"
                for product in products]
    album_id = vk_api.get_album_id()
    vk_api.post_group_wall(photos, captions, album_id=album_id)


if __name__ == "__main__":
    main()
