class Input:

    def __init__(self):
        """ Initialise error messages """

        self.MSG_NO_NUMBER = "You entered a letter, please enter a number."
        self.MSG_OUT_OF_RANGE = "Please enter a valid number, from {} to {}."

    def _validate(self, new_input, min, max):
        """ Validate the input """

        if(new_input == 'QUIT'):
            exit()

        try:
            new_input = int(new_input)
        except:
            print(self.MSG_NO_NUMBER)
            return False
        if(min > new_input or new_input > max):
            print(self.MSG_OUT_OF_RANGE.format(str(min), str(max)))
            return False
        else:
            return True

    def set_input(self, text, min, max):
        """ Ask for input, get the input, validate the input and set the
        input. If the input is not validate, rerun the method. """

        new_input = input(text + " ")

        if(self._validate(new_input, min, max)):
            self.new_input = int(new_input)
        else:
            self.set_input(text, min, max)

    def get_input(self, text, min, max):
        """ Launch the set_input() method and return input """

        self.set_input(text, min, max)

        return self.new_input
