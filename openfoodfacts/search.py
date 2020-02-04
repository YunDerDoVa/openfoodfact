from pony.orm import db_session, commit

from .input import Input
from .models import Category, Food, Brand


class SearchProcess:
    """ This process is launched when the user want to search a new
    substitute """

    @db_session
    def __search_categories(self):
        """ Return all cateogries """

        list = []

        for category in Category.select():
            list.append(category)

        return list

    def __print_categories(self, categories):
        """ Print the categories with the id number to allow the interaction
        with the user """

        print("Choose a category :")
        for i in range(len(categories)):
            print(str(i) + " - " + categories[i].name)

    @db_session
    def __search_foods(self, category):
        """ Return all foods containing the choosen category """

        list = []

        for food in Food.select(lambda f: category in f.categories):
            list.append(food)

        return list

    def __print_foods(self, foods):
        """ Print the foods with the id number to allow the interaction with
        the user """

        print("Choose a food :")
        for i in range(len(foods)):
            print(str(i) + " - " + foods[i].name)

    @db_session
    def __search_substitute(self, food):
        """ Return a substitute of the choosed food """

        return food.find_substitue()

    def __print_substitute(self, food):
        """ Print food infos """

        food.print_infos()

    @db_session
    def __save(self, food):
        """ Save choosen food in favor """

        Food[food.id].favor = True
        commit()

    def run(self):
        """ Run searching processus and interactions """

        input_obj = Input()

        # Get categories
        categories = self.__search_categories()

        # Ask for category
        self.__print_categories(categories)
        text = "Enter the number of your choosen category :"
        input_obj.set_input(text, 0, len(categories))

        # Get foods
        category = categories[input_obj.new_input]
        foods = self.__search_foods(category)

        # Ask for food
        self.__print_foods(foods)
        text = "Enter the number of your choosen food :"
        input_obj.set_input(text, 0, len(foods))

        # Get substitute
        food = foods[input_obj.new_input]
        substitute = self.__search_substitute(food)
        self.__print_substitute(substitute)

        # Ask for save
        text = "Do you want to save this substitute ? No (0) / Yes (1)"
        input_obj.set_input(text, 0, 1)

        # Save
        if input_obj.new_input == 1:
            self.__save(substitute)
