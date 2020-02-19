from pony.orm import db_session

from .input import Input
from .models import Food


class FavorProcess:

    def __init__(self):
        """ Init this class by getting all favors """

        self.favors = self.__search_favors()

    @db_session
    def __search_favors(self):
        """ This method return a list of Favor. """
        list = []

        for substitute in Food.select(lambda f: len(f.substitutes) > 0):
            list.append(substitute)

        return list

    def __print_favors(self):
        """ This method print a list of Favor. """

        print('Your favored food :')
        for i in range(len(self.favors)):
            print(str(i) + ' - ' + self.favors[i].name)

    @db_session
    def __print_favor(self, favor):
        """ This method print a Favor. """

        print("#########################")
        favor.print_infos()

        substitutes = []
        for substitute in Food[favor.id].substitutes:
            substitutes.append(substitute)

            print("#########################")
            print("########## Substitute")
            print("########## id : " + str(len(substitutes)))
            print("########## name : " + substitute.name)
            print("#####-----")
            substitute.print_infos()

        return substitutes

    @db_session
    def __delete(self, favor, substitutes, id):
        """ This method delete a Favor from the database. """

        Food[favor.id].substitutes.remove(Food[substitutes[id].id])

    def run(self):
        """ This method run the process to allow the user to find his
        favor. """

        if len(self.favors) == 0:
            print("You don't have favor yet. Please save a substitute before")
            exit(0)

        input_obj = Input()

        self.__print_favors()

        text = "Enter the number of your favored food :"
        input_obj.set_input(text, 0, len(self.favors))
        favor = self.favors[input_obj.new_input]

        substitutes = self.__print_favor(favor)

        text = (
            "Do you want to delete this favor ?"
            + " No (0) / Yes (id of substitute)"
        )
        input_obj.set_input(text, 0, len(substitutes))
        if(input_obj.new_input > 0):
            self.__delete(favor, substitutes, input_obj.new_input - 1)
