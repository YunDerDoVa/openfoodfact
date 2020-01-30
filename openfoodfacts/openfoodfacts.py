from pony.orm import db_session, commit
import json
import requests

from .models import Food, Category, Brand
from . import settings

class OpenFoodFacts:

    def __init__(self):
        self.products = []
        self.foods = []

    def __fetch_products(self, category):
        print('Fetching ' + category)

        url = 'https://fr-en.openfoodfacts.org/category/'+category+'.json'
        r = requests.get(str(url))
        page = json.loads(r.text)

        number_of_pages = int(page['count']/page['page_size'])
        if(number_of_pages > 50):
            number_of_pages = 50
        if(settings.DEBUG):
            number_of_pages = 1

        print(str(number_of_pages) + ' pages')

        for index_page in range(number_of_pages):
            print('#####\npage ' + str(index_page+1) + '/' + str(number_of_pages))

            url = 'https://fr-en.openfoodfacts.org/category/'+category+'/'+str(index_page+1)+'.json'
            r = requests.get(str(url))
            page = json.loads(r.text)

            for index_page_product in range(page['page_size']):
                print('product ' + str(index_page_product+1) + '/' + str(page['page_size']))

                self.products.append(page['products'][index_page_product])

    def __product_to_food(self, product):

        # Test if json contains all required tags
        name = product['product_name']
        code = product['code']
        nutriments = product['nutriments']
        brands = product['brands']
        categories = product['categories_tags']

        # Insert Food Entity in database
        food = Food(
            name=product['product_name'],
            code=product['code'],
            nutriments=product['nutriments'],
        )

        #
        for brand_name in product['brands'].split(','):
            if(Brand.exists(name=brand_name)):
                brand = Brand.select(lambda b: b.name == brand_name).first()
            else:
                brand = Brand(name=brand_name)
            if(brand != None):
                brand.foods.add(food)

        for category_name in product['categories_tags']:
            if(Category.exists(name=category_name)):
                category = Category.select(lambda c: c.name == category_name).first()
            else:
                category = Category(name=category_name)
            category.foods.add(food)

        commit()
        return food

    def get_food(self, id):
        return self.__product_to_food(self.products[id])

    def fetch_products_list(self, list):
        for name in list:
            self.__fetch_products(name)

    @db_session
    def fill_database(self):
        # Fill products list
        self.fetch_products_list(['pizzas', 'pies', 'fruits', 'vegetables', 'fresh-foods', 'chocolates', 'sugars'])

        # Convert products to Relationnals Entities
        for index_product in range(len(self.products)):
            print('Food ' + str(index_product+1) + '/' + str(len(self.products)))

            try:
                food = self.get_food(index_product)
                self.foods.append(food)
                print('[get_food] Success')
            except:
                print('[get_food] Error')

        self.wash_foods()
        self.wash_categories()
        self.wash_brands()

    def wash_foods(self):

        # Wash Food Entities
        for food in Food.select():
            if(not food.test_food()):
                food.delete()
                print('Food deleted')
            elif(len(Food.select(lambda f: f.code == food.code)) > 1):
                food.delete()
                print('Food deleted')
            elif(len(food.brands) == 0):
                food.delete()
                print('Food deleted')

    def wash_categories(self):

        # Wash Category Entities
        for category in Category.select():
            if(len(category.foods) == 0):
                category.delete()
                print('Category deleted')

    def wash_brands(self):

        # Wash Brand Entities
        for brand in Brand.select():
            if(len(brand.foods) == 0):
                brand.delete()
                print('Brand deleted')
