import sys
from pony.orm import *

from . import settings
from .settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

db = Database()

class Food(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Set('Category')
    brands = Set('Brand')
    code = Required(str)
    nutriments = Required(Json)
    favor = Optional('Favor')

class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)

class Brand(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    foods = Set(Food)

class Favor(db.Entity):
    id = PrimaryKey(int, auto=True)
    food = Required(Food)

db.bind(provider='mysql', host=MYSQL_HOST, user=MYSQL_USER,
    passwd=MYSQL_PASSWORD, db=MYSQL_DB)
db.generate_mapping(create_tables=True)

if(settings.DEBUG):
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
