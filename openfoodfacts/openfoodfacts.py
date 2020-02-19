import json
import requests
from pony.orm import db_session, commit

from .models import Food, Category, Brand, Store
from . import settings


class ProductDownloader:
    """ This class download products form the openfoodfacts api. """

    def __init__(self):
        """ Initialise products list """
        self.products = []

    def __fetch_products(self, category):
        """ Get all products from the openfoodfacts api. """

        print("Fetching " + category)

        url = (
            "https://world.openfoodfacts.org/cgi/search.pl"
        )
        payload = {
            'search_terms': category,
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 10
        }
        r = requests.get(str(url), payload)
        page = json.loads(r.text)

        # Define page size
        page_size = 1000
        if settings.DEBUG:
            page_size = 20

        # Calcul number of pages
        number_of_pages = int(int(page["count"]) / page_size)
        if settings.DEBUG:
            number_of_pages = 1

        print(str(page['count']) + " products")
        print(str(number_of_pages) + " pages")

        payload['page_size'] = page_size
        for index_page in range(number_of_pages):
            print("##### " + str(category))
            print(
                "##### page "
                + str(index_page + 1)
                + "/"
                + str(number_of_pages)
            )

            payload['page'] = index_page
            r = requests.get(str(url), payload)
            page = json.loads(r.text)

            page_count = page_size
            if int(page["count"]) - page_size * index_page < 0:
                page_count = page['count'] % page_size

            for index_page_product in range(page_count):
                if settings.VERB:
                    print(
                        "product "
                        + str(index_page_product + 1)
                        + "/"
                        + str(page["page_size"])
                    )

                self.products.append(page["products"][index_page_product])

    def fetch_products_list(self, list):
        """ Take a list of categories in argument.
        Launch __fetch_products(category) method for each category in the
        list and return the internal list of products """

        for name in list:
            self.__fetch_products(name)

        return self.products


class DBWasher:
    """ This class wash the database. """

    @db_session
    def wash_foods(self):
        """ Wash Food Entities """

        for food in Food.select():
            if not food.test_food():
                food.delete()
                print("Food deleted")
            elif len(Food.select(lambda f: f.code == food.code)) > 1:
                food.delete()
                print("Food deleted")
            elif len(food.brands) == 0:
                food.delete()
                print("Food deleted")

    @db_session
    def wash_categories(self):
        """ Wash Category Entities """

        for category in Category.select():
            if len(category.foods) == 0:
                category.delete()
                print("Category deleted")

    @db_session
    def wash_brands(self):
        """ Wash Brand Entities """

        for brand in Brand.select():
            if len(brand.foods) == 0:
                brand.delete()
                print("Brand deleted")

    @db_session
    def wash_stores(self):
        """ Wash Store Entities """

        for store in Store.select():
            if len(store.foods) == 0:
                store.delete()
                print("Store deleted")


class DBFiller:
    """ This class is specialised to fill the database """

    @db_session
    def insert_food_from_product(self, product):
        """ Cast product (object from openfoodfacts json) to a Food Entity and
        insert this Entity in the database. This method is made of 6
        steps : """

        """ 1. Get all necessaries tags """
        name = product["product_name"]
        code = product["code"]
        nutriments = product["nutriments"]
        brands = product["brands"]
        categories = product["categories_tags"]
        stores = product['stores']

        """2.  Insert Food Entity in database """
        food = Food(
            name=name,
            code=code,
            nutriments=nutriments,
        )

        """ 3. Insert Brand if don't exists and link this Brand to the Food """
        for brand_name in brands.split(","):
            if Brand.exists(name=brand_name):
                brand = Brand.select(lambda b: b.name == brand_name).first()
            else:
                brand = Brand(name=brand_name)
            if brand is not None:
                brand.foods.add(food)

        """ 4. Insert Category if don't exists and link it to the Food """
        for category_name in categories:
            if Category.exists(name=category_name):
                category = Category.select(
                    lambda c: c.name == category_name
                ).first()
            else:
                category = Category(name=category_name)
            category.foods.add(food)

        """ 5. Insert Store if don't exists and link it to the Food """
        for store_name in stores:
            if Store.exists(name=store_name):
                store = Store.select(
                    lambda c: c.name == store_name
                ).first()
            else:
                store = Store(name=store_name)
            store.foods.add(food)

        """ 6. Commit Entities """
        commit()


class OpenFoodFacts:
    """ This class set the database up before the using of the program. """

    def fill_database(self):
        """ It fill the database with some categories of food """

        # Fill products list
        downloader = ProductDownloader()
        products = downloader.fetch_products_list(
            [
                "fruits",
                "legumes",
                "frais",
                "sucres",
                "boissons",
                "viandes",
                "laits",
            ]
        )

        # Convert products to Relationnals Entities
        filler = DBFiller()
        for index_product in range(len(products)):
            print(
                "Food "
                + str(index_product + 1)
                + "/"
                + str(len(products))
            )

            try:
                filler.insert_food_from_product(products[index_product])
                print("[insert_food_from_product] Success")
            except BaseException:
                print("[insert_food_from_product] Error")

        # Wash Database
        washer = DBWasher()
        washer.wash_foods()
        washer.wash_categories()
        washer.wash_brands()
        washer.wash_stores()
