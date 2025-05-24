import random
from enemies import Enemy
from evennia import AttributeProperty

class Scout(Enemy):
    """
    A scout type human enemy with a small healthpool and high speed.
    """
    physical = AttributeProperty(random.randint(1, 10))
    mental = AttributeProperty(random.randint(1, 10))
    social = AttributeProperty(random.randint(1, 10))

    hp = AttributeProperty(random.randint(5, 15))
    hp_max = AttributeProperty(hp)
    #Stamina may not be needed for combat npcs

    level = AttributeProperty(1)

    def at_object_creation(self):
        super.at_object_creation

    def set_level(self, level):
        self.level = level
        self.set_stats(level)

    def set_stats(self, level):
        multiplier = random.randint(1, level) / level
        self.physical = self.physical * multiplier
        self.mental = self.mental * multiplier
        self.social = self.social * multiplier
        self.hp = self.hp * multiplier
        self.hp_max = self.hp