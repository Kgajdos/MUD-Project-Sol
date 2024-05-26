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


class Drone(Enemy):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.health = random.randint(700,1500)
        self.db.sheilds = random.randint(1000,3300)

    def at_char_entered(self, character):
        if self.db.is_aggresive:
            self.execute_cmd("The drone is targetting you!")
        else:
            self.execute_cmd("The drone passes by.")
