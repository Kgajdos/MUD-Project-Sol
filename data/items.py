from evennia import DefaultObject
from enum import Enum

class ToolQuality(Enum):
    POOR = 0.01
    LOW = 0.05
    MED = 0.10
    GOOD = 0.15
    GREAT = 0.20
    EXTRAORDINARY = 0.25

BS_HELMET = {
    "prototype_key": "BS_HELMET",
    "key": "BS Helmet",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["helmet"],
    "attrs": [("desc", "A helmet made by Basic Space. Are those dents?"),
              ("armor_slot", "head"),
              ("quality", ToolQuality.POOR)],
}

BS_SUIT = {
    "prototype_key": "BS_SUIT",
    "key": "BS Suit",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["suit"],
    "attrs": [("desc", "A space suit designed by Basic Space. I'm sure that's not a stain."),
              ("armor_slot", "body"),
              ("quality", ToolQuality.POOR)],
}

BS_GLOVES = {
    "prototype_key": "BS_GLOVES",
    "key": "BS Gloves",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["gloves"],
    "attrs": [("desc", "Gloves made by Basic Space. Hopefully your fingers won't freeze out there."),
              ("armor_slot", "arms"),
              ("quality", ToolQuality.POOR)],
}

BS_BOOTS = {
    "prototype_key": "BS_BOOTS",
    "key": "BS Boots",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["boots"],
    "attrs": [("desc", "Boots designed by Basic Space. They don't look very comfortable."),
              ("armor_slot", "feet"),
              ("quality", ToolQuality.POOR)],
}

BS_RIFLE = {
    "prototype_key": "BS_RIFLE",
    "key": "BS Rifle",
    "value": 100,
    "aliases": ["riffle"],
    "typeclass": "typeclasses.weapons.Gun",
    "attrs": [("desc", "A rifle designed by Basic Space. It seems kind of light and flimsy."),
              ("armor_slot", "hands"),
              ("quality", ToolQuality.POOR)],
}

BS_DRINK = {
    "prototype_key": "BS_DRINK",
    "key": "BS Drink",
    "value": 10,
    "typeclass": "typeclasses.drinkables.Drinkable",
    "attrs": [("desc", "A drink designed by Basic Space. The taste is awful, but promises improved focus!"),
              ("quality", ToolQuality.POOR)
              ("effects", "mental")],
}

BS_STEW = {
    "prototype_key": "BS_STEW",
    "key": "BS Stew",
    "value": 10,
    "typeclass": "typeclasses.eatables.Eatable",
    "attrs": [("desc", "A stew designed by Basic Space. It has an odd smell, but promises good health!"),
              ("quality", ToolQuality.POOR)
              ("effects", "health")],
}

BS_MULTITOOL = {
    "prototype_key": "BS_MULTITOOL",
    "key": "Multitool",
    "value": 100,
    "typeclasses": "typeclasses.tools.Tools",
    "attrs": [("desc", "A tool designed to handle multiple jobs. Using one increases working efficiency."),
              ("quality", ToolQuality.POOR)],
}

BS_TABLE = {
    "prototype_key": "BS_TABLE",
    "key": "BS Table",
    "value": 10,
    "typeclasses": "typeclasses.objects.Object",
    "attrs": [("desc", "A simple metal table of poor quality. It looks like it will fall apart soon."),
              ("quality", ToolQuality.POOR)],
}

BS_CHAIR = {
    "prototype_key": "BS_CHAIR",
    "key": "BS Chair",
    "value": 10,
    "typeclasses": "typeclasses.sitables.Sitable",
    "attrs": [("desc", "A simple metal chair of poor quality. Can it even handle my weight?"),
              ("quality", ToolQuality.POOR)],
}

BS_BED = {
    "prototype_key": "BS_BED",
    "key": "BS Bed",
    "value": 100,
    "typeclasses": "typeclasses.sitables.Layable",
    "attrs": [("desc", "A simple metal bed made of poor quality. The stuffing looks thin..."),
              ("quality", ToolQuality.POOR)]
}