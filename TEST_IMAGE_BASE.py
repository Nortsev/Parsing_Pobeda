import base_sqllite as sql
import shutil
import os
import vk_api_pobeda as post

conn = sql.create_connection()
IMAGE_DIR = 'img'
get_image_sql = '''SELECT title , price , photo FROM top_items ORDER BY retrieved_time DESC LIMIT {img_count}'''


def write_image(file_name, img):
    try:
        with open(file_name, "wb") as f:
            f.write(img)
    except IOError as error:
        print(error)
        return False

    return True


def export_image(conn, img_count=5):
    sql_query = get_image_sql.format(img_count=img_count)
    result = []
    if os.path.exists(IMAGE_DIR):
        shutil.rmtree(IMAGE_DIR)

    os.mkdir(IMAGE_DIR)
    cur = conn.cursor()
    image_name = 1
    products_info = cur.execute(sql_query)
    for product in products_info:
        image_path = f'{IMAGE_DIR}/{image_name}.jpg'
        write_image(image_path, product[2])
        result.append({'title': product[0],
                       'price': product[1],
                       'image': image_path})
        image_name += 1
    return result


def start():
    export_image(conn)
