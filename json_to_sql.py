# -tc- Pourquoi ce module n'appartient-il pas au package openfoodfacts?

# -tc- Attention à définir des docstrings de module, de classe, de méthode et
# -tc- de fonction. Dans ce projet en doc-driven development, tu es supposé
# -tc- écrire les docstrings avant d'implémenter les méthodes!!!

# -tc- attention à formater les imports correctement
import json
import requests

# -tc- éviter le wildcard dans les imports
from pony.orm import *

# -tc- utiliser un fichier de config séparé ou des variables d'environnement
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "openfoodfacts"

db = Database()

# -tc- Je ne suis pas convaincu par l'usage d'un type json pour stocker les infos
# -tc- sur les catégories, dénormalisant ainsi la base de données inutilement.
# -tc- la bonne pratique serait d'utiliser une classe séparée et une relation
# -tc- plusieurs à plusieurs. Idem pour les infos sur les magasins (ce n'est
# pas vraiment brand qui nous intéresse, mais stores)
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

    # -tc- La pratique courante est de n'utiliser que un seul underscore pour
    # -tc- les méthodes privées.
    def __fetch_products(self, category):
        # -tc- Pourquoi ne pas utiliser l'API de recherche pour pouvoir
        # -tc- télécharger plus de 20 produits à la fois (jusqu'à 1000)?
        url = "https://fr-en.openfoodfacts.org/category/" + category + ".json"
        r = requests.get(str(url))
        page = json.loads(r.text)

        number_of_pages = int(page["count"] / page["page_size"])

        # Uncomment this line to launch a speed fetch
        # number_of_pages = 1

        # -tc- Tu te complique à mon avis la vie, car il suffit de télécharger
        # -tc- une page de 1000 produits
        print(str(number_of_pages) + " pages")

        for index_page in range(number_of_pages):
            print(
                "#####\npage "
                + str(index_page + 1)
                + "/"
                + str(number_of_pages)
            )

            url = (
                "https://fr-en.openfoodfacts.org/category/"
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

    # -tc- Que se passe-t-il si product ne contient pas toutes les infos?
    def __product_to_food(self, product):
        food = Food(
            name=product["product_name"],
            categories=product["categories_tags"],
            brands=product["brands"],
            code=product["code"],
            nutriments=product["nutriments"],
        )
        return food

    def __get_food(self, id):
        return self.__product_to_food(self.products[id])

    # -tc- Une même classe ne devrait pas à la fois se charger de télécharger
    # -tc- les données sur l'API, de les nettoyer et des les insérer en base.
    # -tc- Concevoir des classes séparées pour chacune de ces responsabilités.
    # -tc- Une classe == une responsabilité
    @db_session
    def fill_database(self):
        self.__fetch_products("pizzas")
        self.__fetch_products("pies")

        for index_product in range(len(self.products)):
            print(str(index_product + 1) + "/" + str(len(self.products)))
            try:
                self.foods.append(self.__get_food(index_product))
                print("Yes")
            except:
                print("No")


# -tc- Ne pas ajouter de code exécutable au niveau global du module.
db.bind(
    provider="mysql",
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DB,
)
db.generate_mapping(create_tables=True)

openfoodfacts = OpenFoodFacts()
# -tc- Je n'ai pas vu d'étape de nettoyage. A ajouter
openfoodfacts.fill_database()
