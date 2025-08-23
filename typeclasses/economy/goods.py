from evennia import DefaultObject
from evennia.utils.utils import AttributeProperty

class Good(DefaultObject):
    """
    Represents a unit of tradeable, processable material or product in the economy.
    Goods can be raw materials, refined components, or finished products.
    """

    def at_object_creation(self):
        stage = AttributeProperty(default="raw")
        origin = AttributeProperty(default=None)
        tags = AttributeProperty(default=[])
        volume = AttributeProperty(default=1)
        weight = AttributeProperty(default=1)
        value = AttributeProperty(default=0)
        process_history = AttributeProperty(default=[])

        self.set_description()

    def set_description(self):
        self.db.desc = f"{self.key} ({self.stage})"
        if self.orgin:
            desc += f" - Origin: {self.origin}"
    
    def can_be_processed_at(self, station_type):
        from .recipes import GOOD_PROCESSING_RECIPES
        recipe = GOOD_PROCESSING_RECIPES.get(self.key)
        return recipe and recipe.get("station") == station_type