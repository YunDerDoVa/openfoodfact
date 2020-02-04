import json
import requests
from pony.orm import db_session, commit

from .models import Food, Category, Brand
from . import settings


class ProductDownloader:
    """ This class download products form the openfoodfacts api. """

    def __init__(self):
        """ Initialise products list """
        self.products = []

    def __fetch_products(self, category):
        """ Get all products from the openfoodfacts api. """

        print("Fetching " + category)

        url = "https://fr.openfoodfacts.org/categorie/" + category + ".json"
        r = requests.get(str(url))
        page = json.loads(r.text)

        number_of_pages = int(page["count"] / page["page_size"])
        if number_of_pages > 100:
            number_of_pages = 100
        if settings.DEBUG:
            number_of_pages = 1

        print(str(number_of_pages) + " pages")

        for index_page in range(number_of_pages):
            print("##### " + str(category))
            print(
                "##### page "
                + str(index_page + 1)
                + "/"
                + str(number_of_pages)
            )

            url = (
                "https://fr.openfoodfacts.org/categorie/"
                + category
                + "/"
                + str(index_page + 1)
                + ".json"
            )
            r = requests.get(str(url))
            page = json.loads(r.text)

            for index_page_product in range(page["page_size"]):
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


class DBFiller:
    """ This class is specialised to fill the database """

    @db_session
    def insert_food_from_product(self, product):
        """ Cast product (object from openfoodfacts json) to a Food Entity and
        insert this Entity in the database. This method is made of 5 steps : """

        """ 1. Get all necessaries tags """
        name = product["product_name"]
        code = product["code"]
        nutriments = product["nutriments"]
        brands = product["brands"]
        categories = product["categories_tags"]

        """2.  Insert Food Entity in database """
        food = Food(
            name=product["product_name"],
            code=product["code"],
            nutriments=product["nutriments"],
        )

        """ 3. Insert Brand if it don't exists and link this Brand to the Food """
        for brand_name in product["brands"].split(","):
            if Brand.exists(name=brand_name):
                brand = Brand.select(lambda b: b.name == brand_name).first()
            else:
                brand = Brand(name=brand_name)
            if brand != None:
                brand.foods.add(food)

        """ 4. Insert Category if it don't exists and link it to the Food """
        for category_name in product["categories_tags"]:
            if Category.exists(name=category_name):
                category = Category.select(
                    lambda c: c.name == category_name
                ).first()
            else:
                category = Category(name=category_name)
            category.foods.add(food)

        """ 5. Commit Entities """
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
                "legumes-et-derives",
#                "frais",
#                "sucres",
#                "boissons",
#                "viandes",
#                "laits",
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
            except:
                print("[insert_food_from_product] Error")

        # Wash Database
        washer = DBWasher()
        washer.wash_foods()
        washer.wash_categories()
        washer.wash_brands()
