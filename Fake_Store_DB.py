import sqlite3 as sq


class FakeStoreDb:
    def __init__(self):
        self.database = 'database.db'

    def create_product_table(self):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER,
                title TEXT,
                price REAL,
                category TEXT,
                description TEXT,
                image TEXT,
                rating_rate REAL,
                rating_count INTEGER,
                user_id INTEGER
            )
            ''')

    def insert_product(self, product_id, title, description, price, category, image, rating_rate, rating_count, user_id):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()
            cursor.execute('''
                INSERT INTO product (id, title, description, price, category, image, rating_rate, rating_count, user_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, title, description, price, category, image, rating_rate, rating_count, user_id))

    def insert_all_products(self, products):
        for product in products:
            self.insert_product(
                product['id'],
                product['title'],
                product['description'],
                product['price'],
                product['category'],
                product['image'],
                product['rating']['rate'],
                product['rating']['count'],
                product['user_id']
            )

    def insert_product_by_id(self, product_id, user_id, products):
        for product in products:
            if product['id'] == int(product_id):
                self.insert_product(
                    product['id'],
                    product['title'],
                    product['description'],
                    product['price'],
                    product['category'],
                    product['image'],
                    product['rating']['rate'],
                    product['rating']['count'],
                    user_id
                )

    def delete_product_by_id(self, product_id, user_id, products):
        for product in products:
            if product['id'] == int(product_id):
                with sq.connect(self.database) as connect:
                    cursor = connect.cursor()
                    cursor.execute(f'DELETE FROM product WHERE id = {product_id} AND user_id = {user_id}')

    def show_table_product(self, user_id):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()
            cursor.execute(f'SELECT id, title, price FROM product WHERE user_id = {user_id}')
            data = cursor.fetchall()
            return data

    def delete_all_products(self, user_id):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()
            cursor.execute(f'DELETE FROM product WHERE user_id = {user_id}')

    def delete_table(self, user_id):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()
            cursor.execute(f'DROP TABLE IF EXISTS product WHERE user_id = {user_id}')

    def is_table_empty(self, user_id):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()
            cursor.execute(f'SELECT count(*) FROM product WHERE user_id = {user_id}')
            res = cursor.fetchone()
        if res[0] == 0:
            return True
        else:
            return False

    def is_product_exist(self, product_id, user_id):
        with sq.connect(self.database) as connect:
            cursor = connect.cursor()
            cursor.execute(f'SELECT count(id) FROM product WHERE id = {product_id} AND user_id = {user_id}')
            res = cursor.fetchone()
        if res[0] == 1:
            return True
        else:
            return False
