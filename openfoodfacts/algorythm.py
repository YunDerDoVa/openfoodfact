import math

class Algorythm:

    matrice = [1, 1, 2, 1, 1, 2, 2, 1, 1, 5]

    def __init__(self, food_1, food_2):
        self.nutriments_data_1 = Algorythm.get_nutriments_data(food_1)
        self.nutriments_data_2 = Algorythm.get_nutriments_data(food_2)

    @staticmethod
    def get_nutriments_data(food):
        data = [
            float(food.nutriments['fat']),
            float(food.nutriments['salt']),
            float(food.nutriments['energy_100g']),
            float(food.nutriments['sodium']),
            float(food.nutriments['sugars']),
            float(food.nutriments['proteins_100g']),
            float(food.nutriments['fiber']),
            float(food.nutriments['carbohydrates_100g']),
            float(food.nutriments['nutrition-score-fr_100g']),
        ]

        return data

    def compare_datas(self):

        #print("Comparing\n" + str(self.nutriments_data_1) + "\nand\n" + str(self.nutriments_data_2))

        list = []

        for i in range(len(self.nutriments_data_1)):
            score = self.nutriments_data_1[i] - self.nutriments_data_2[i]
            list.append(score * Algorythm.matrice[i])

        return list

    def get_score(self):
        score = 0

        for num in self.compare_datas():
            score += num*num

        return score
