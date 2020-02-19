import sys
import math
import random

from pony.orm import Database, db_session
from pony.orm import PrimaryKey, Required, Set, Json

from .settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from .algorythm import Algorythm


db = Database()


class Food(db.Entity):
    """ Food Class contains the data of openfoodfacts """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Set("Category")
    brands = Set("Brand")
    stores = Set("Store")
    code = Required(str)
    nutriments = Required(Json)
    substitutes_of = Set('Food', reverse='substitutes')
    substitutes = Set('Food', reverse='substitutes_of')

    @db_session
    def print_infos(self):
        """ This method print all infos of the food, the method __str__ is
        not used because she is even used by ponyORM and we prefer let ponyORM
        use it to develope in better conditions """

        brands = Brand.select(lambda b: self in b.foods)
        stores = Store.select(lambda s: self in s.foods)

        print("##### Name : " + self.name)
        print(
            "##### Link : https://world.openfoodfacts.org/product/"
            + self.code
        )
        print("##### Brands :")
        for brand in brands:
            print("##### \t- " + brand.name)
        if len(stores) > 0:
            print("Stores :")
            for store in stores:
                print("##### \t- " + store.name)
        print("#########################\n")

    def test_substitute(self, food, power):
        """ This method test if the current object is compatible with the
        pood passed in argument and the given power
        (power is a arbitrary value who quantify the difference between
        foods) """

        algorythm = Algorythm(self, food)

        if algorythm.get_score() > power:
            return False
        else:
            return True

    def find_substitue(self):
        """ This method find a substitute of the current object """

        substitutes = Food.select(lambda f: f != self)
        searching = True
        counter = 0.0
        match_list = []

        if not self.test_food():
            print("This food is not valid, here is your food stats.")
            return self

        while searching:
            counter += 0.1
            power = math.exp(counter)

            for substitute in substitutes:
                if substitute not in Food[self.id].substitutes:
                    if self.test_substitute(substitute, power):
                        print("Divergence power : " + str(power))
                        match_list.append(substitute)

            if len(match_list) > 0:
                print(str(len(match_list)) + ' substitutes found...')
                return match_list[int(random.random() * (len(match_list) - 1))]

            if power > math.exp(100):
                print("No substitute found, here is your food stats.")
                return self

    def test_food(self):
        """ This method test if the food have all required data to find
        substitute """

        try:
            Algorythm.get_nutriments_data(self)
            return True
        except BaseException:
            return False


class Category(db.Entity):
    """ Category Class is connected to food by a many-to-many relation. """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)


class Brand(db.Entity):
    """ Brand Class is connected to food by a many-to-many relation. """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)


class Store(db.Entity):
    """ Store Class is connected to food by a many-to-many relation """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)


# Connect to database
db.bind(
    provider="mysql",
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DB,
)

# Generate database mapping and create tables if they doesn't exists
db.generate_mapping(create_tables=True)

# This lines delete and rebuild the tables if we fill the database
if len(sys.argv) > 0:
    if "fill_database" in sys.argv:
        db.drop_all_tables(with_all_data=True)
        db.create_tables()
