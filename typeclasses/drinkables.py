from evennia import create_object
from typeclasses.objects import Object

class Drinkables(Object):
    #Effects should be a dict with keys as attributes and values as their modifiers (positive or negative)
    def at_object_creation(self):
         self.db.name = ""
         self.db.desc = ""
         self.db.attributes = {}

    def create_drink(self, name, desc, **effects):
         self.db.name = name
         self.db.desc = desc
         self.add_effect(effects)
    
    def add_effect(self, **effects):
        for attr, mod in effects:
                self.db.attribute[attr] = mod
    
    def drink(self, caller):
        for attribute, modifier in self.db.attribute:
             caller.db.attribute[attribute] += modifier