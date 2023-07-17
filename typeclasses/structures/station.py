from typeclasses.objects import Object
from evennia import utils

class Station(Object):
    """
    TODO: docs
    """
    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        #this is checking if it is a PC
        if moved_obj.account:
            #this is informing all npcs in the room
            moved_obj.msg(f"Welcome aboard Captain {moved_obj.key}.")