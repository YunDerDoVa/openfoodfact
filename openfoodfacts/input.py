class Input:

    def __init__(self):
        self.MSG_NO_NUMBER = "You entered a letter, please enter a number."
        self.MSG_OUT_OF_RANGE = "Please enter a valid number, from {} to {}."

    def _validate(self, new_input, min, max):
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
        new_input = input(text + " ")

        if(self._validate(new_input, min, max)):
            self.new_input = int(new_input)
        else:
            self.set_input(text, min, max)
