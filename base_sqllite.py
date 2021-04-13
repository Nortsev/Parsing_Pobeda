"""SQLite3 library"""
import sqlite3


database_file = 'post_vk.db'
sql_create = """ CREATE TABLE IF NOT EXISTS top_items(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    retrieved_time DATE DEFAULT (datetime('now','localtime')),
                    title TEXT NOT NULL,
                    price TEXT NOT NULL,
                    url TEXT NOT NULL,
                    url_photo TEXT NOT NULL,
                    photo BLOB NOT NULL
                );"""


def create_connection(database=database_file):
    """Create connection to database"""
    conn = None
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute(sql_create)
    except Exception as e:
        print(f'ERROR: {e}')
    return conn


def insert_products(conn, products: list) -> bool:
    """Insert a list of products to database"""
    try:
        sql = """INSERT INTO top_items(title,price,url,url_photo,photo) VALUES(?, ?, ?, ?, ?)"""
        cur = conn.cursor()
        for product in products:
            cur.execute(sql, list(product.values()))
            conn.commit()
    except Exception as e:
        print(f'ERROR: {e}')
        return False
    return True







