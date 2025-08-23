import random
from typeclasses.objects import Object
from evennia import create_object

rarity_point_values = {
    "Common": [10, 100],
    "Uncommon": [100, 1000],
    "Rare": [1000, 10000]
}

class Anomoly(Object):
    """
    This is the start of the anomoly class.
    """

    def at_object_creation(self):
        """
        Called when the resource is first created.
        """
        #Points refers to anomoly points that players can "scan" from the Anomoly
        self.db.points = 0
        self.tags.add("Research Points")
        self.db.rarity = self.choose_rarity()

    def choose_rarity(self):
        rarities = ["Common", "Uncommon", "Rare"]
        weights = [64, 24, 8]
        return random.choices(rarities, weights=weights, k=1)[0]
    
    def set_research_points(self):
        rarity = self.db.rarity
        self.db.points = random.randint(*rarity_point_values[rarity])
    
    @classmethod
    def generate_anomoly(cls):
        """
        Generate a new anomoly with a random yet weighted amount of Research Points
        """
        anomoly = create_object(typeclass = "typeclasses.anomolies.Anomoly", key = "Anomoly")
        anomoly.db.points = anomoly.choose_rarity()
        anomoly.set_research_points()
        return anomoly