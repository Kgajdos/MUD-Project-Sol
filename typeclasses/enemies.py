import evennia
from evennia.objects import Object
from typeclasses.characters import Character
import random

class Enemy(Character, Object):
    """
    As this is not a combat focused game yet, enemies will be very simple.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.physical = random.randint(1,10)
        self.db.mental = random.randint(1,10)

    def at_char_entered(self, character):
        """
        A simple is_aggressive check.
        Expand upon later - and make it more flexible
        """
        #This block here will need to be changed, it's way too static
        if self.db.is_aggressive:
            self.execute_cmd("SQUEEEK!")
        else:
            self.execute_cmd("squeek.")