from .input import Input

class FavorProcess:

    def __init__(self):
        self.favors = self.__search_favors()

    def __search_favors(self):
        """ This method return a list of Favor. """

        return Favor.select()

    def __print_favors(self):
        """ This method print a list of Favor. """

        print('Your favored food :')
        for i in range(len(self.favors)):
            print(str(i) + ' - ' + self.favors.name)

    def __get_favor(self, id):
        """ This method return a Favor taking the argument of the Favor. """

        return self.favors[id]

    def __print_favor(self, favor):
        """ This method print a Favor. """

        favor.print_infos()

    def __delete(self, favor):
        """ This method delete a Favor from the database. """

        favor.delete()

    def run(self):
        """ This method run the process to allow the user to find his favor. """

        input_obj = Input()

        self.__print_favors()

        text = "Enter the number of your favored food :"
        new_input = input_obj(text, 1, len(favors))
        favor = self.__get_favor(new_input)

        self.__print_favor(favor)

        text = "Test 2"
        new_input = input_obj(text, 0, 1)
        if(new_input == 1):
            self.delete(favor)
