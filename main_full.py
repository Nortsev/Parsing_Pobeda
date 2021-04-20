# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import base_sqllite as sql
import TEST_IMAGE_BASE as save_img
import vk_api_pobeda as vk_api

ALBUM_NAME = 'Repost'
link = [

    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/telefony/sotovye-telefony/?k=false&q=20&s=high&c=57&cg=143&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/?k=false&q=20&s=high&c=57&cg=99&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?k=false&q=20&s=high&c=57&cg=84&a=0&f[]=400&",
    "https://энгельс.победа-63.рф/catalog/avto/?k=false&q=20&s=high&c=57&cg=132&a=0&f[]=400&",

]
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
        if "noimage" in image_path:
            continue

        title = item.find('meta', attrs={"itemprop": "name"})['content']
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

    conn = sql.create_connection()
    sql.insert_products(conn, products)

    return products


def main():
    html = get_html(random.choice(link))
    if html.status_code != 200:
        print("Error conect")

    get_content(html.text)
    products = save_img.start()
    photos = [product['image'] for product in products]
    captions = [f"{product['title']} \n  Цена: {product['price']} \n Ссылка на товар на нашем сайте: {product['url']}"
                for product in products]
    create_session = vk_api.create_session()
    album_id = vk_api.get_album_id(create_session, ALBUM_NAME)
    vk_api.post_group_wall(photos, captions, album_id=album_id)


if __name__ == "__main__":
    main()
