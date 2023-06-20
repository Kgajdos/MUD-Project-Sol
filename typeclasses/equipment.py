from enums import WieldLocation, Ability
from typeclasses.objects import get_bare_hands, ProjectSolObject
from evennia.utils.utils import inherits_from

class EquipmentError(TypeError):
    pass


class EquipmentHandler:
    save_attribute = "inventory_slots"

    def __init__(self, obj):
        #here obj is the character
        self.obj = obj
        self._load()

    def _load(self):
        """Load our data from an Attribute on self.obj"""
        self.slots = self.obj.attributes.get(
            self.save_attribute,
            category = "inventory",
            default={
                WieldLocation.WEAPON_HAND: None, 
                WieldLocation.TWO_HANDED: None,
                WieldLocation.OFF_HAND: None, 
                WieldLocation.BODY: None,
                WieldLocation.HEAD: None,
                WieldLocation.FEET: None,
                WieldLocation.BACKPACK: []
            } 
        )
    def _save(self):
        """Save our data back to the same Attribute"""
        self.obj.attributes.add(self.save_attribute, self.slots, category = "inventory")

    @property
    def max_slots(self):
        """Max amount of slots, based on CON defense (CON + 10)"""
        return getattr(self.obj, Ability.PHY.value, 1) + 10
    
    def count_slots(self):
        """Count current slot usage"""
        slots = self.slots
        wield_usage = sum(
            getattr(slotobj, "size", 0) or 0
            for slot, slotobj in slots.items()
            if slot is not WieldLocation.BACKPACK
        )
        backpack_usage = sum(
            getattr(slotobj, "size", 0) or 0 for slotobj in slots[WieldLocation.BACKPACK]
        )
        return wield_usage + backpack_usage
    
    def validate_slot_usage(self, obj):
        """
        Check if obj can fit in equipment, based on its size.
          
        """
        if not inherits_from(obj, ProjectSolObject):
        # in case we mix with non-evadventure objects
            raise EquipmentError(f"{obj.key} is not something that can be equipped.")
  
        size = obj.size
        max_slots = self.max_slots
        current_slot_usage = self.count_slots()
        return current_slot_usage + size <= max_slots
    
    def add(self, obj):
        """Put something in the backpack"""
        self.validate_slot_usage(obj)
        self.slots[WieldLocation.BACKPACK].append(obj)
        self._save()

    def remove(self, slot):
        """Removes contents of a particular slot, for example
        `equipment.remove(WieldLocation.SHIELD_HAND)`"""
        slots = self.slots
        ret = []
        if slot is WieldLocation.BACKPACK:
            #empty entire backback
            ret.extend(slots[slot])
            slots[slots] = []
        else:
            ret.append(slots[slot])
            slots[slot] = None
        if ret:
            self._save()
        return ret
    def move(self, obj):
        """Move an object from the backpack to its intended inventory slot"""
        #make sure to remove form equipment/backpack first to avoid double - adding
        self.remove(obj)

        slots = self.slots
        use_slot = getattr(obj, "inventory_use_slot", WieldLocation.BACKPACK)

        to_backpack = []
        if use_slot is WieldLocation.TWO_HANDS:
            #Two handed cant be wielded with a shield or other sword
            to_backpack = [slots[WieldLocation.WEAPON_HAND], slots[WieldLocation.OFF_HAND]]
            slots[WieldLocation.WEAPON_HAND] = slots[WieldLocation.OFF_HAND]
            slots[use_slot] = obj
        elif use_slot in (WieldLocation.WEAPON_HAND, WieldLocation.OFF_HAND):
            #cant keep a two hander if adding a sword/shield
            to_backpack = [slots[WieldLocation.TWO_HANDED]]
            slots[WieldLocation.TWO_HANDED] = None
            slots[use_slot] = obj
        elif use_slot is WieldLocation.BACKPACK:
            #It belongs in backpack, so it goes back to it
            to_backpack = [obj]
        else:
            #for others (body, head), just replace whatever's there
            replaced = [obj]
            slots[use_slot] = obj

        for to_backpack_obj in to_backpack:
            #Put stuff in backpack
            slots[use_slot].append(to_backpack_obj)

        #store new save state
        self._save()

    def all(self):
        """Get all objects in inventory, regardless of location"""
        slots = self.slots
        lst = [
            (slots[WieldLocation.WEAPON_HAND], WieldLocation.WEAPON_HAND),
            (slots[WieldLocation.OFF_HAND], WieldLocation.OFF_HAND),
            (slots[WieldLocation.FEET], WieldLocation.FEET),
            (slots[WieldLocation.TWO_HANDED], WieldLocation.TWO_HANDED),
            (slots[WieldLocation.BODY], WieldLocation.BODY),
            (slots[WieldLocation.HEAD], WieldLocation.HEAD),
        ] + [(item, WieldLocation.BACKPACK) for item in slots[WieldLocation.BACKPACK]]
        return lst
    
    @property
    def armor(self):
        slots = self.slots
        return sum(
            (
                # armor is listed using its defense, so we remove 10 from it
                # (11 is base no-armor value in Knave)
                getattr(slots[WieldLocation.BODY], "armor", 1),
                # shields and helmets are listed by their bonus to armor
                getattr(slots[WieldLocation.FEET], "armor", 0),
                getattr(slots[WieldLocation.HEAD], "armor", 0),
            )
        )
    @property
    def weapon(self):
        #first checks two hander, then one
        slots = self.slots
        weapon = slots[WieldLocation.TWO_HANDED]
        if not weapon:
            weapon = slots[WieldLocation.WEAPON_HAND]
        #if we still dont have a weapon, we return none here
        if not weapon:
            weapon = get_bare_hands()