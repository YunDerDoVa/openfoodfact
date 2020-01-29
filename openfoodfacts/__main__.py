import sys

from .openfoodfacts import OpenFoodFacts
from .input import Input
from .favor import FavorProcess
from .search import SearchProcess

def check_argv():
    """ This function the arguments. If 'fill_database' is passed
    in command, it initialise the OpenFoodFacts class and fill the database
    with the OpenFoodFacts REST api. """

    if(len(sys.argv) > 0):
        if('fill_database' in sys.argv):
            openfoodfacts = OpenFoodFacts()
            openfoodfacts.fill_database()

def run_program():
    """ This function run the program, asking a simple question. """

    input_obj = Input()

    text = 'Find substitutes (1) or go to the favori-list (2) ?'
    input_obj.set_input(text, 1, 2)
    if(input_obj.new_input == 1):
        search_process = SearchProcess()
        search_process.run()
    elif(input_obj.new_input == 2):
        favor_process = FavorProcess()
        favor_process.run()

def main():
    check_argv()
    run_program()


if __name__ == "__main__":
    main()
