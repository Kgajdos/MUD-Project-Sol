from enum import Enum

class WieldLocation(Enum):

    BACKPACK = "bag"
    WEAPON_HAND_MAIN = "weapon_hand_main"
    WEAPON_HAND_OFF = "weapon_hand_off"
    TWO_HANDED = "two_handed_weapons"
    BODY = "body" #armor
    HEAD = "head" #helmets

# How to type define the objects to make db storing easier
class ObjType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    VISOR = "visor"
    CONSUMABLE = "consumable"
    GEAR = "gear"
    QUEST = "quest"
    LOOT = "loot"