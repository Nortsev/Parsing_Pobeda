# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import base_sqllite as sql
import TEST_IMAGE_BASE as save_img
import vk_api_pobeda as vk_api

link = [

    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/telefony/sotovye-telefony/?k=false&q=20&s=high&c=57&cg=143&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/?k=false&q=20&s=high&c=57&cg=99&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?k=false&q=20&s=high&c=57&cg=84&a=0&f[]=400&"
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
    save_img.start()
    photos = ["img/1.jpg", "img/2.jpg", "img/3.jpg", "img/4.jpg", "img/5.jpg"]
    captions = ['1\ntest', '2', '3', '4', '5']
    vk_api.post_group_wall(photos, captions, album_id=279184675)


if __name__ == "__main__":
    main()


