from evennia import utils, TICKER_HANDLER, create_object
from typeclasses.asteroids import Asteroid
import random

def create_new_room():
    # Define the possible room types
    room_types = ["asteroid_field", "nebula", "planet", "anomaly"]
    
    # Define descriptions for each room type
    DESCRIPTIONS = {
        "asteroid_field": [
            "A dense asteroid field surrounds you, with massive rocks floating ominously.",
            "The ship navigates through a chaotic asteroid belt, with debris scattering around.",
            "You are in the midst of a violent asteroid storm, with rocks tumbling past at high speed."
        ],
        "nebula": [
            "A colorful nebula stretches across the void, with vibrant gases swirling in beautiful patterns.",
            "The nebula is dense and mysterious, with light filtering through clouds of interstellar dust.",
            "You drift through a vast nebula, with shimmering colors and ethereal light."
        ],
        "planet": [
            "A distant planet looms ahead, its surface covered in swirling clouds.",
            "You approach a planet with a striking blue hue, its surface teeming with mystery.",
            "A rocky planet orbits here, with a barren landscape visible through the ship's viewports."
        ],
        "anomaly": [
            "A strange anomaly distorts the space around it, with odd gravitational effects and light patterns.",
            "You encounter an enigmatic space anomaly, its nature defying easy explanation.",
            "The anomaly creates unusual readings on your instruments, with space-time seemingly warped around it."
        ]
    }
    
    # Choose a random room type
    room_type = random.choice(room_types)
    
    # Get the descriptions for the chosen room type
    descriptions = DESCRIPTIONS.get(room_type, [])
    
    # Pick a random description
    if descriptions:
        description = random.choice(descriptions)
    else:
        description = "An unknown area of space."

    # Create the new room with the selected description
    new_room = create_object("typeclasses.rooms.SpaceRoom", key=room_type)
    new_room.db.desc = description

    return new_room
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

class TutorialRoom(Room):
    """
    Only to be used for the spawning room! Needed to allow mission hook
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "This is the tutorial room. You can learn how to play the game here."

        # Create some objects to interact with
        map = create_object("typeclasses.objects.Object", key="Map", location=self, attributes=[("desc", "A map with directions pointing to the Hangers. It reads:\n")])
        cup = create_object("typeclasses.objects.Object", key="Cup", location=self, attributes=[("desc", "A shiny red apple. Looks delicious.")])

    def at_object_receive(self, moved_obj, source_location, move_type="move", **kwargs):
        if moved_obj.account:
            #this is informing all npcs in the room
            for item in self.contents:
                if utils.inherits_from(item, "typeclasses.npc.NPC"):
                    item.at_char_entered(moved_obj)
            from missions.first_steps import mission_setup
            if not moved_obj.tags.has("captain"):
                mission_setup(moved_obj)


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
    