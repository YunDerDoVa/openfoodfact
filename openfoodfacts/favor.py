from .input import Input

class Favor:

    def __init__(self):
        self.favors = self.__search_favors()

    def __search_favors(self):
        """ This method return a list of Favor. """

        pass

    def __print_favors(self):
        """ This method print a list of Favor. """

        pass

    def __get_favor(self, id):
        """ This method return a Favor taking the argument of the Favor. """

        pass

    def __print_favor(self, favor):
        """ This method print a Favor. """

        favor.print_infos()
        pass

    def __delete(self, favor):
        """ This method delete a Favor from the database. """

        pass

    def run(self):
        """ This method run the process to allow the user to find his favor. """

        input_obj = Input()

        self.__print_favors()

        text = "Test"
        new_input = input_obj(text, 1, len(favors))
        favor = self.get_favor(new_input)

        self.__print_favor(favor)

        text = "Test 2"
        new_input = input_obj(text, 0, 1)
        if(new_input == 1):
            self.delete(favor)
