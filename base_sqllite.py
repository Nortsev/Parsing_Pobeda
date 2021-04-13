import sqlite3


database_file = 'post_vk.db'
sql_create = """ CREATE TABLE IF NOT EXISTS top_items(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price TEXT NOT NULL,
                    url TEXT NOT NULL,
                    url_photo TEXT NOT NULL,
                    photo BLOB NOT NULL,
                    date_parsing TIME NOT NULL
                );"""


def create_database(database=database_file):
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_create)
    except Exception as e:
        print(f'ERROR: {e}')
    return conn


def insert_products(conn, products):
    try:
        sql = """INSERT INTO top_items(title,price,url,url_photo,photo,date_parsing) VALUES(?, ?, ?, ?, ?, ?)"""
        cur = conn.cursor()
        for product in products:
            cur.execute(sql, list(product.values()))
            conn.commit()
        return True
    except Exception as e:
        print(f'ERROR: {e}')
        return False







