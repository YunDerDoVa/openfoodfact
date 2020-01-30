import sys
from pony.orm import *
import math

from .settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from .algorythm import Algorythm

db = Database()

class Food(db.Entity):
    """ Food Class contains the data of openfoodfacts """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Set('Category')
    brands = Set('Brand')
    code = Required(str)
    nutriments = Required(Json)
    favor = Optional(bool)

    @db_session
    def print_infos(self):
        brands = Brand.select(lambda b: self in b.foods)

        print("Name : " + self.name)
        print("Description : " + self.code)
        print("Brands :")
        for brand in brands:
            print("\t- " + brand.name)

    def test_substitute(self, food, power):

        algorythm = Algorythm(self, food)

        if(algorythm.get_score() > power):
            return False
        else:
            return True

    def find_substitue(self):
        substitutes = Food.select(lambda f: f != self)
        searching = True
        counter = 0.0

        if(not self.test_food()):
            print('This food is not valid, here is your food stats.')
            return self

        while(searching):
            counter += 0.1
            power = math.exp(counter)
            for substitute in substitutes:
                if(substitute.test_substitute(self, power)):
                    print('Divergence power : ' + str(power))
                    return substitute

            if(power > math.exp(100)):
                print('No substitute found, here is your food stats.')
                return self

    def test_food(self):
        try:
            Algorythm.get_nutriments_data(self)
            return True
        except:
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

# Connect to database
db.bind(provider='mysql', host=MYSQL_HOST, user=MYSQL_USER,
    passwd=MYSQL_PASSWORD, db=MYSQL_DB)

# Generate database mapping and create tables if they doesn't exists
db.generate_mapping(create_tables=True)

# This lines delete and rebuild the tables if we fill the database
if(len(sys.argv) > 0):
    if('fill_database' in sys.argv):
        db.drop_all_tables(with_all_data=True)
        db.create_tables()
