from evennia import create_object
from evennia.utils import evmenu
from typeclasses.objects import Object


def _add_effect(caller, raw_input_,**kwargs):
     effect = kwargs.get("attribute")
     caller.msg(f"Creating Drink that alters {effect}")
     

def node_add_drink_effect(caller, raw_input, **kwargs):
     text = "Pick an attribute for the drink to effect."
     options = (
          {"key": ("[H]ealth", "health", "h"),
           "desc": "Alters health.",
           "goto": _add_effect, "attribute": "health"},
           {"key": ("[S]tamina", "stamina", "s"),
            "desc": "Alters stamina",
            "goto": _add_effect, "attribute": "stamina"},
            {"key": ("[P]ysical", "physical", "p"),
            "desc": "Alters physical",
            "goto": _add_effect, "attribute": "physical"},
            {"key": ("[M]ental", "mental", "m"),
            "desc": "Alters mental",
            "goto": _add_effect, "attribute": "mental"},
            {"key": ("[S]ocial", "social"),
            "desc": "Alters social",
            "goto": _add_effect, "attribute": "social"},
     )

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
    
    def add_effect(self, effects):
        for attr, mod in effects:
                self.db.attribute[attr] = mod
    
    def drink(self, caller):
        for attribute, modifier in self.db.attribute:
             caller.db.attribute[attribute] += modifier

