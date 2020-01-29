from pony.orm import db_session, commit

from .input import Input
from .models import Category, Food, Brand


class SearchProcess:

    def __init__(self):
        self.categories = self.__search_categories()
        self.foods = []

    @db_session
    def __search_categories(self):
        list = []

        for category in Category.select():
            list.append(category)

        return list

    def __print_categories(self):
        print("Choose a category :")
        for i in range(len(self.categories)):
            print(str(i) + ' - ' + self.categories[i].name)

    @db_session
    def __search_foods(self, id):
        category = self.categories[id]

        list = []

        for food in Food.select(lambda f: category in f.categories):
            list.append(food)

        return list

    def __print_foods(self, foods):
        print("Choose a food :")
        for i in range(len(foods)):
            print(str(i) + ' - ' + foods[i].name)

    @db_session
    def __search_substitute(self, food):

        substitutes = Food.select(lambda f: f != food)

        list = []
        power = 0

        while(len(list) == 0):
            power += 0.1
            for substitute in substitutes:
                if(substitute.test_substitute(food, power)):
                    list.append(substitute)

        print('Divergence power : ' + str(power))
        return list[0]

    def __print_substitute(self, food):
        food.print_infos()

    @db_session
    def __save(self, food):
        Food[food.id].favor = True
        commit()

    def run(self):
        input_obj = Input()

        # Ask for category
        self.__print_categories()
        text = "Enter the number of your choosen category :"
        input_obj.set_input(text, 0, len(self.categories))

        # Get foods
        foods = self.__search_foods(input_obj.new_input)

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
        if(input_obj.new_input == 1):
            self.__save(substitute)
