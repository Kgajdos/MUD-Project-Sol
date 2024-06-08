from evennia import utils, TICKER_HANDLER
from typeclasses.asteroids import Asteroid
import random
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
                    item.at_char_entered(moved_obj)


class SpaceRoom(Room):
    """
    A specific room type in Project Sol where the majority of "gameplay" happens.
    """
    def at_object_creation(self):
        """
        This method is called when the room is created.

        Notes:
            - It generates a random number of asteroids (1-10) and adds them to the room.
        """
        TICKER_HANDLER.add(60 * 3, self.check_and_add_asteroid) #makes a check every hours worth of seconds the ticker has run
        asteroid_count = random.randint(1, 10)
        for _ in range(asteroid_count):
            self.add_asteroid()




    def check_and_add_asteroid(self):
        """
        Checks the number of asteroids in the room and adds one if it is less than 10.

        Notes:
            - This method is called periodically by the ticker handler.
        """
        asteroid_count = self.get_asteroid_count()


        if asteroid_count < 10:
            # Add an asteroid to the room
            self.add_asteroid()

    def get_asteroid_count(self):
        """
        Counts the number of asteroids in the room.

        Returns:
            int: The count of asteroids in the room.
        """
        return len([obj for obj in self.contents if obj.key.lower() == "asteroid"])

    def add_asteroid(self):
        """
        Adds a new asteroid to the room.

        Notes:
            - It generates random resource quantities for the asteroid and sets its location to the room.
            - It also sends a message to all characters in the room about the newly added asteroid.
        """
        #resource_dict = {resource.value for resource in Resource}
        asteroid = Asteroid.generate_asteroid()
        asteroid.location = self
        self.msg_contents("An asteroid drifts into view.")

    def warp_player_to_random_room(self, player):
        #Retrieve all existing rooms from the database
        existing_rooms = Room.objects.all()

        #Choose a random existing room and move the player there
        existing_room = random.choice(existing_rooms)
        player.move_to(existing_room)

class ShipStorageRoom(Room):

    def at_object_creation(self):
        self.db.cargo = {}

    def return_room_contents(self):
        contents = {}
        for obj in self.db.contents:
            key = obj.key
            quantity = obj.db.quantity
            contents[key] = quantity
        return contents
    