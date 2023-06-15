#Custom engine for Project Sol
from random import randint
from enums import Ability

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

def heal_from_rest(self, character):
     """
     A night's rest retains 1d8 + CON HP
     """
     con_bonus = getattr(character, Ability.CON.value, 1)
     character.heal(self.roll("1d8" + con_bonus))

def roll_random_table(self, dieroll, table_choices): 
        """ 
        Args: 
             dieroll (str): A die roll string, like "1d20".
             table_choices (iterable): A list of either single elements or 
                of tuples.
        Returns: 
            Any: A random result from the given list of choices.
            
        Raises:
            RuntimeError: If rolling dice giving results outside the table.
            
        """
        roll_result = self.roll(dieroll) 
        
        if isinstance(table_choices[0], (tuple, list)):
            # the first element is a tuple/list; treat as on the form [("1-5", "item"),...]
            for (valrange, choice) in table_choices:
                minval, *maxval = valrange.split("-", 1)
                minval = abs(int(minval))
                maxval = abs(int(maxval[0]) if maxval else minval)
                
                if minval <= roll_result <= maxval:
                    return choice 
                # if we get here we must have set a dieroll producing a value 
            # outside of the table boundaries - raise error
            raise RuntimeError("roll_random_table: Invalid die roll")
        else:
            # a simple regular list
            roll_result = max(1, min(len(table_choices), roll_result))
            return table_choices[roll_result - 1]
        
dice = ProjectSolRollEngine()