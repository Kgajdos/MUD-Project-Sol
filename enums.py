from enum import Enum

class Ability(Enum):
    """
    The three abilities:
    """
    PHY = "physical"
    MEN = "mental"
    SOC = "social"

    ARMOR = "armor"

    CRITICAL_FAILURE = "critical_failure"
    CRITICAL_SUCCESS = "critical_success"

    ALLEGIANCE_HOSTILE = "hostile"
    ALLEGIANCE_NEUTRAL = "neutral"
    ALLEGIANCE_FRIENDLY = "friendly"

ABILITY_REVERSE_MAP = {
    "phy": Ability.PHY,
    "men": Ability.MEN,
    "soc": Ability.SOC
}

class WieldLocation(Enum):

    BACKPACK = "bag"
    WEAPON_HAND = "weapon_hand"
    OFF_HAND = "off_hand"
    TWO_HANDED = "two_handed_weapons"
    BODY = "body" #armor
    HEAD = "head" #helmets
    ARMS = "arms"#Gloves, bracers, ect
    FEET = "feet"

# How to type define the objects to make db storing easier
class ObjType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    VISOR = "visor"
    CONSUMABLE = "consumable"
    GEAR = "gear"
    QUEST = "quest"
    LOOT = "loot"