import unittest
import create_date_base

def sql_api():
    sql_api = create_date_base.SQLApi()

class TestCreateConnection(unittest.TestCase):
    def test_create_connection(self):
        res = create_date_base.SQLApi.create_connection(self)
        self.assertEqual(isinstance(res, object), True)

    def test_insert_products(self):
        product = {'title': 'Xiaomi Redmi 9 4/64GB (NFC)', 'price': '8990',
                   'url': 'https://xn--80aag1ciek.xn---030500153980/',
                   'url_photo': 'https://xn--c1aesfx9dc.xn---63-5cdesg4ei._8-705-440.webp',
                   'photo': 'img/1.jpg'}
        
        res = create_date_base.SQLApi.insert_products(self, product)
        print('test')
        self.assertEqual(res, True)

    # def test_get_images(self):
    #     res = create_date_base.SQLApi.get_images(self, 5)
    #     self.assertEqual(isinstance(res, list), True)

if __name__ == "__main__":
    unittest.main()
