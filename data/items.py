from evennia import DefaultObject
from enum import Enum

class ToolQuality(Enum):
    POOR = 0.01
    LOW = 0.05
    MED = 0.10
    GOOD = 0.15
    GREAT = 0.20
    EXTRAORDINARY = 0.25

