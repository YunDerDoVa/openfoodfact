import json
import requests

class Food:
    def __init__(self, name):
        self.name = name

class OpenFoodFacts:

    DEBUG = True

    def __init__(self):

        self.products = []

        self.__fetch_products('pizzas')
        self.__wash_products()

    def __fetch_products(self, category):
        url = 'https://fr-en.openfoodfacts.org/category/'+category+'.json'
        r = requests.get(str(url))
        page = json.loads(r.text)

        number_of_pages = int(page['count']/page['page_size'])
        print(str(number_of_pages) + ' pages')

        for index_page in range(number_of_pages):
            print('#####\npage ' + str(index_page+1) + '/' + str(number_of_pages))

            url = 'https://fr-en.openfoodfacts.org/category/'+category+'/'+str(index_page+1)+'.json'
            r = requests.get(str(url))
            page = json.loads(r.text)

            for index_page_product in range(page['page_size']):
                print('product ' + str(index_page_product+1) + '/' + str(page['page_size']))

                self.products.append(page['products'][index_page_product])

    def __wash_products(self):
        count = 0
        for product in self.products:
            count += 1

        print(str(count) + ' products washed')

    def __product_to_food(self, product):
        food = Food(product['product_name'])
        print(food.name)

    def get_food(self, id):
        return self.__product_to_food(self.products[id])


openfoodfacts = OpenFoodFacts()

print(openfoodfacts.get_food(42))
