from enum import Enum

class Ability(Enum):
    """
    The three abilities:
    """
    PHY = "physical"
    MEN = "mental"
    SOC = "social"
    HEL = "health"
    STA = "stamina"

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
    RESOURCE = "resource"

class ToolQuality(Enum):
    POOR = 0.01
    LOW = 0.05
    MED = 0.10
    GOOD = 0.15
    GREAT = 0.20
    EXTRORDINARY = 0.25

class Resource(Enum):
    IRON = ("iron", "common")
    NICKLE = ("nickle", "common")
    CLAY = ("clay", "common")
    HYDROGEN = ("hydrogen", "common")

    SILVER = ("silver", "uncommon")
    WOOD = ("woord", "uncommon")
    HELIUM = ("helium", "uncommon")

    GOLD = ("gold", "rare")
    PLATINUM = ("platinum", "rare")
    SILICATE = ("silicate", "rare")
    PLASMA = ("plasma", "rare")

class SHIP(Enum):
    MAIN_GUN = "main_gun"
    ALT_GUN = "alt_gun"
    MAIN_ROCKET = "main_rocket"
    ALT_ROCKET = "alt_rocket"
    CARGO = {}