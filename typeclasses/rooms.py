from evennia import utils
"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        #this is checking if it is a PC
        if moved_obj.account:
            #this is informing all npcs in the room
            for item in self.contents:
                if utils.inherits_from(item, "typeclasses.npc.NPC"):
                    self.at_char_entered(moved_obj)
