import requests


class FakeStoreAPI:

    def __init__(self):
        self.url = 'https://fakestoreapi.com/products/'

    def get_all_products(self):
        return requests.get(self.url).json()

    def get_product_by_id(self, product_id):
        return requests.get(f'{self.url}{product_id}').json()

    def get_limited_results(self, limit):
        params = {"limit": limit}
        return requests.get(f'{self.url}', params=params).json()

    def get_sorted_products_by_id(self, key):
        params = {"sort": key}
        return requests.get(f'{self.url}', params=params).json()

    def get_all_categories(self):
        return requests.get(self.url + 'categories').json()

    def get_product_in_specific_category(self, category):
        return requests.get(f'{self.url}category/{category}').json()

    def get_products_by_category(self):
        data = []
        for i in self.get_all_categories():
            data.append(self.get_product_in_specific_category(i))
        return data
