from FakeStore import FakeStoreAPI
from Fake_Store_DB import FakeStoreDb

fakestoreapi = FakeStoreAPI()
fakestoredb = FakeStoreDb()


def get_all_products():
    data = fakestoreapi.get_all_products()
    result = ''
    for product in data:
        result += f'''
*ID:* {product['id']}
*Название:* {product['title']}
*Цена:* {product['price']}$
'''
    return result


def get_all_categories():
    data = fakestoreapi.get_all_categories()
    return data


def get_product_in_category(category):
    data = fakestoreapi.get_product_in_specific_category(category)
    result = ''
    for product in data:
        result += f'''
*ID:* {product['id']}
*Название:* {product['title']}
*Цена:* {product['price']}$
'''
    return result


def create_table():
    fakestoredb.create_product_table()


def save_product_to_db(product_id, user_id):
    fakestoredb.create_product_table()
    fakestoredb.insert_product_by_id(product_id, user_id, fakestoreapi.get_all_products())


def show_table(user_id):
    products = fakestoredb.show_table_product(user_id)
    result = ''
    for product in products:
        result += f'''
*ID:* {product[0]}
*Название:* {product[1]}
*Цена:* {product[2]}$
'''
    return result


def delete_product(product_id, user_id):
    fakestoredb.delete_product_by_id(product_id, user_id, fakestoreapi.get_all_products())


def is_empty(user_id):
    if fakestoredb.is_table_empty(user_id):
        return True
    return False


def is_exist(product_id, user_id):
    if fakestoredb.is_product_exist(product_id, user_id):
        return True
    return False


def delete_all(user_id):
    fakestoredb.delete_all_products(user_id)
