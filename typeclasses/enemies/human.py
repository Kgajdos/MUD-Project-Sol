import random
from enemies import Enemy
from evennia import AttributeProperty

class Scout(Enemy):
    """
    A scout type human enemy with a small healthpool and high speed.
    """
    # set non-random defaults at class level; initialize per-instance in at_object_creation
    physical = AttributeProperty(0)
    mental = AttributeProperty(0)
    social = AttributeProperty(0)

    hp = AttributeProperty(0)
    hp_max = AttributeProperty(0)
    #Stamina may not be needed for combat npcs

    level = AttributeProperty(1)

    def at_object_creation(self):
        # ensure base setup runs
        super().at_object_creation()
        # initialize randomized stats per-enemy instance
        self.physical = random.randint(1, 10)
        self.mental = random.randint(1, 10)
        self.social = random.randint(1, 10)

        self.hp = random.randint(5, 15)
        self.hp_max = self.hp

    def set_level(self, level):
        self.level = level
        self.set_stats(level)

    def set_stats(self, level):
        if level <= 0:
            return
        multiplier = random.randint(1, max(1, level)) / float(level)
        # ensure we keep integer stats
        self.physical = int(self.physical * multiplier)
        self.mental = int(self.mental * multiplier)
        self.social = int(self.social * multiplier)
        self.hp = int(self.hp * multiplier)
        self.hp_max = self.hp