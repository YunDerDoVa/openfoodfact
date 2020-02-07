# -tc- algorithm s'écrit avec un i

# -tc- documenter le code à l'aide de docstrings au niveau module, classe,
# -tc- méthode et fonction
import math

# -tc- pas convaincu par l'algorithme. Je me réjouis de discuter les résultats
# -tc- en session


class Algorythm:
    """ This class calcul datas of two foods to determine the real proximity
    of the differents nutriments into the food """

    matrice = [1, 1, 2, 1, 1, 2, 2, 1, 1, 5]

    def __init__(self, food_1, food_2):
        """ init method takes two foods in argument """

        self.nutriments_data_1 = Algorythm.get_nutriments_data(food_1)
        self.nutriments_data_2 = Algorythm.get_nutriments_data(food_2)

    @staticmethod
    def get_nutriments_data(food):
        """ Its static method return a dict having all required
        nutritive data to run the algorithme """

        data = [
            float(food.nutriments["fat"]),
            float(food.nutriments["salt"]),
            float(food.nutriments["energy_100g"]),
            float(food.nutriments["sodium"]),
            float(food.nutriments["sugars"]),
            float(food.nutriments["proteins_100g"]),
            float(food.nutriments["fiber"]),
            float(food.nutriments["carbohydrates_100g"]),
            float(food.nutriments["nutrition-score-fr_100g"]),
        ]

        return data

    def compare_datas(self):
        """ This method return a array of scores """

        list = []

        for i in range(len(self.nutriments_data_1)):
            score = self.nutriments_data_1[i] - self.nutriments_data_2[i]
            list.append(score * Algorythm.matrice[i])

        return list

    def get_score(self):
        """ This method return a score who represent an arbitrary difference
        between the two foods of this class """

        score = 0

        for num in self.compare_datas():
            score += num * num

        return score
