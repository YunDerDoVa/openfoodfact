from pony.orm import db_session

from .input import Input
from .models import Food

class FavorProcess:

    def __init__(self):
        self.favors = self.__search_favors()

    @db_session
    def __search_favors(self):
        """ This method return a list of Favor. """
        list = []

        for favor in Food.select(lambda f: f.favor == True):
            list.append(favor)

        return list

    def __print_favors(self):
        """ This method print a list of Favor. """

        print('Your favored food :')
        for i in range(len(self.favors)):
            print(str(i) + ' - ' + self.favors[i].name)

    def __get_favor(self, id):
        """ This method return a Favor taking the argument of the Favor. """

        return self.favors[id]

    def __print_favor(self, favor):
        """ This method print a Favor. """

        favor.print_infos()

    @db_session
    def __delete(self, favor):
        """ This method delete a Favor from the database. """

        Food[favor.id].delete()

    def run(self):
        """ This method run the process to allow the user to find his favor. """

        input_obj = Input()

        self.__print_favors()

        text = "Enter the number of your favored food :"
        input_obj.set_input(text, 0, len(self.favors))
        favor = self.__get_favor(input_obj.new_input)

        self.__print_favor(favor)

        text = "Do you want to delete this favor ? No (0) / Yes (1)"
        input_obj.set_input(text, 0, 1)
        if(input_obj.new_input == 1):
            self.__delete(favor)
