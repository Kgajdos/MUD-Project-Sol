#Practice engine using the Knave rules
from random import randint


class RollEngine:

    def roll(self, roll_string):
        """ 
        Roll XdY dice, where X is the number of dice 
        and Y the number of sides per die. 
        
        Args:
            roll_string (str): A dice string on the form XdY.
        Returns:
            int: The result of the roll. 
            
        """ 
        
        # split the XdY input on the 'd' one time
        number, diesize = roll_string.split("d", 1)     
        
        # convert from string to integers
        number = int(number) 
        diesize = int(diesize)
            
        # make the roll
        return sum(randint(1, diesize) for _ in range(number))

    def roll_with_advantage_or_disadvantage(self, advantage=False, disadvantage=False):
        
        if not (advantage or disadvantage) or (advantage and disadvantage):
            #normal roll -advantage/disadvantage not set or cancel each other out
            return self.roll("1d20")
        elif advantage:
            #highest of two d20 rolls
            return max(self.roll("1d20"), self.roll("1d20"))
        else:
            #disadvantage - lowest of two d20 rolls
            return min(self.roll("1d20"), self.roll("1d20"))

    def saving_throw(self, character, target=15, 
                     advantage=False, disadvantage=False):
                # make a roll 
        dice_roll = self.roll_with_advantage_or_disadvantage(advantage, disadvantage)
       
       # figure out if we had critical failure/success
        quality = None
        if dice_roll == 1:
           quality = Ability.CRITICAL_FAILURE
        elif dice_roll == 20:
           quality = Ability.CRITICAL_SUCCESS 

       # figure out bonus
        #bonus = getattr(character, bonus_type.value, 1) 

       # return a tuple (bool, quality)
        return (dice_roll) > target, quality
        """ 
       Do a saving throw, trying to beat a target.
       
       Args:
          character (Character): A character (assumed to have Ability bonuses
              stored on itself as Attributes).
          bonus_type (Ability): A valid Ability bonus enum.
          target (int): The target number to beat. Always 15 in Knave.
          advantage (bool): If character has advantage on this roll.
          disadvantage (bool): If character has disadvantage on this roll.
          
       Returns:
           tuple: A tuple (bool, Ability), showing if the throw succeeded and 
               the quality is one of None or Ability.CRITICAL_FAILURE/SUCCESS
               
        """             


    #def opposed_saving_throw(...):

    #def roll_random_table(...):

    #def morale_check(...):

    #def heal_from_rest(...):

    def roll_death(self, character):
        ability_name = self.roll_random_table("1d8", death_table)

        if ability_name == "dead":
            character.at_death()
        else:

            if current_ability < -10:
                character.at_death()
            else:
                


                dice = ProjectSolRollEngine()