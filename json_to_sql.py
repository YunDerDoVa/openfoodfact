import json
import requests
from pony.orm import *

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'openfoodfacts'

db = Database()

class Food(db.Entity):

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Required(Json)
    brands = Required(str)
    code = Required(str)
    nutriments = Required(Json)


class OpenFoodFacts:

    def __init__(self):
        self.products = []
        self.foods = []

    def __fetch_products(self, category):
        url = 'https://fr-en.openfoodfacts.org/category/'+category+'.json'
        r = requests.get(str(url))
        page = json.loads(r.text)

        number_of_pages = int(page['count']/page['page_size'])

        # Uncomment this line to launch a speed fetch
        #number_of_pages = 1

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
        food = Food(
            name=product['product_name'],
            categories=product['categories_tags'],
            brands=product['brands'],
            code=product['code'],
            nutriments=product['nutriments'],
        )
        return food

    def __get_food(self, id):
        return self.__product_to_food(self.products[id])

    @db_session
    def fill_database(self):
        self.__fetch_products('pizzas')
        self.__fetch_products('pies')

        for index_product in range(len(self.products)):
            print(str(index_product+1) + '/' + str(len(self.products)))
            try:
                self.foods.append(self.__get_food(index_product))
                print('Yes')
            except:
                print('No')


db.bind(provider='mysql', host=MYSQL_HOST, user=MYSQL_USER,
    passwd=MYSQL_PASSWORD, db=MYSQL_DB)
db.generate_mapping(create_tables=True)

openfoodfacts = OpenFoodFacts()
openfoodfacts.fill_database()
