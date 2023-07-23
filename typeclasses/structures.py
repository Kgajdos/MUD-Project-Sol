from typeclasses.objects import Object
from typeclasses.rooms import Room
from evennia import create_object, utils

class Structure(Object):
    """
    Represents a structure in the game world.

    Methods:
        at_object_creation(): Called when the structure is first created.
        at_object_receive(moved_obj, source_location, move_type="move", **kwargs): Called when an object is moved into the structure.
        create_room(roomname, exits, destination): Creates a new room within the structure.
        docking(player): Informs the player that docking is granted and begins the docking process.
        undocking(player): Informs the player that they are undocking from the structure.

    Notes:
        - This class is intended to be subclassed for specific types of structures in the game.
        - Structures are objects that can contain other objects, such as rooms, items, or characters.
    """
    def at_object_creation(self):
        pass

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        """
        Called when an object is moved into the structure.

        Args:
            moved_obj (Object): The object that was moved into the structure.
            source_location (Object): The previous location of the moved object.
            move_type (str, optional): The type of move that occurred (e.g., "move", "teleport").
            **kwargs: Additional keyword arguments, if any.

        Notes:
            - If the moved object is a player character (PC), this method will inform all NPCs in the structure.
        """
        #this is checking if it is a PC
        if moved_obj.account:
            #this is informing all npcs in the room
            for item in self.contents:
                if utils.inherits_from(item, "typeclasses.npc.NPC"):
                    self.at_char_entered(moved_obj)
    
    def create_room(self, roomname, exits, destination):
        """
        Creates a new room within the structure.

        Args:
            roomname (str): The name of the new room.
            exits (dict): A dictionary specifying the exits from the new room.
            destination (Object or str): The destination of the new room's exits.

        Notes:
            - This method creates a new room object and adds it as a content of the structure.
        """
        self.create_object(typeclasses = "typeclasses.rooms.Room", key = roomname, exits = exits, destination = destination)

    def docking(self, player):
        """
        Informs the player that docking is granted and begins the docking process.

        Args:
            player (Object): The player character to inform about docking.
        """
        player.msg(f"Docking is granted for {player}. Beginning docking.")

    def undocking(self, player):
        """
        Informs the player that they are undocking from the structure.

        Args:
            player (Object): The player character to inform about undocking.
        """
        player.msg(f"{player} is undocking.")