from evennia import DefaultObject
from enum import Enum
from .components import COMPONENT
from .tools import TOOLS
from .ship_parts import SHIP_PARTS
from .consumables import CONSUMABLES

ITEM_DEFINITIONS = {
    **COMPONENT,
    **TOOLS,
    **SHIP_PARTS,
    **CONSUMABLES
}

class ItemCategory(Enum):
    COMPONENT = "component"
    TOOL = "tool"
    STRUCTURE = "structure"
    SHIP_PART = "ship_part"
    CONSUMABLE = "consumable"

class ManufacturedItem(DefaultObject):
    def at_object_creation(self):
        self.db.materials = {}
        self.db.production_time = 0
        self.db.required_research = None
        self.db.category = ItemCategory.COMPONENT.value
        self.db.market_value = 0
        self.db.quality = None

class ToolQuality(Enum):
    POOR = 0.01
    LOW = 0.05
    MED = 0.10
    GOOD = 0.15
    GREAT = 0.20
    EXTRAORDINARY = 0.25
