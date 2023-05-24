#Custom engine for Project Sol
from random import randint

class ProjectSolRollEngine:

    def roll(self, roll_string):
        """
        Roll xdY dice, where x is the number of dice and Y is the number of sides

        Args:
            roll_string(str): A dice string on the form xdY
        Returns:
            int: The result of the roll
        """

        #split the xdY input by the d
        number, diesize = roll_string.split("d", 1)

        #convert from string to int
        number = int(number)
        diesize = int(diesize)

        #make the roll
        return sum(randint(1, diesize) for _ in range(number))
