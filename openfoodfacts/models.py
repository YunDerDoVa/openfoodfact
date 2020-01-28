from pony.orm import *

from .database.Pony import db

class Food(db.Entity):

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    categories = Required(Json)
    brands = Required(str)
    code = Required(str)
    nutriments = Required(Json)
