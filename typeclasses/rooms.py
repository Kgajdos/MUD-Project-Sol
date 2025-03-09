from evennia import utils, TICKER_HANDLER, create_object
from typeclasses.asteroids import Asteroid
import random

def generate_room_name(room_type_prefix, unique_number):
    """
    Generate a unique room name with the format 'AA-NNN'.
    
    :param room_type_prefix: Two-letter prefix for the room type (e.g., 'PL' for Planet)
    :param unique_number: Unique number for the room
    :return: Formatted room name
    """
    unique_number_formatted = f"{unique_number:03}"  # Format number as a three-digit string
    room_name = f"{room_type_prefix}-{unique_number_formatted}"
    return room_name

def create_new_room():
    # Define the possible room types and their prefixes
    room_types = {
        "anomaly": "AN",
        "asteroid_field": "AF",
        "nebula": "NE",
        "planet": "PL"
    }

    # Choose a random room type
    room_type_key = random.choice(list(room_types.keys()))
    room_type_prefix = room_types[room_type_key]

    # Generate a unique number for the room
    unique_number = random.randint(1, 999)  # Random number between 1 and 999

    # Generate a unique room name
    room_name = generate_room_name(room_type_prefix, unique_number)

    # Select the room class based on the type
    room_class = {
        "anomaly": AnomalyRoom,
        "asteroid_field": AsteroidRoom,
        "nebula": NebulaRoom,
        "planet": PlanetRoom
    }[room_type_key]

    # Create the new room with the generated name
    new_room = create_object(room_class, key=room_name)

    # Debugging output
    print(f"Debug: Created room '{new_room.key}' of type '{room_type_key}'")

    # Verify if the room can be accessed
    try:
        room = SpaceRoom.objects.get(db_key=new_room.key)
        print(f"Debug: Accessing room details: {room.__dict__}")
    except SpaceRoom.DoesNotExist:
        print("Debug: Room not found in SpaceRoom")
    
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
    A specific room type in Project Sol where the majority of "gameplay" happens. This is the parent class,
    add general functions as needed
    """
    pass

class AsteroidRoom(SpaceRoom):
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

class AnomalyRoom(SpaceRoom):
    """
    This is a room type representing an anomaly in space.
    Anomalies might have special effects or dangers associated with them.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "anomaly"
        self.db.desc = "A strange anomaly distorts the space around it, with odd gravitational effects and light patterns."
        # Add any anomaly-specific initialization here

class NebulaRoom(SpaceRoom):
    """
    This is a room type representing a nebula.
    Nebulas might have special visual effects or hide certain objects.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "nebula"
        self.db.desc = "A colorful nebula stretches across the void, with vibrant gases swirling in beautiful patterns."
        # Add any nebula-specific initialization here

class PlanetRoom(SpaceRoom):
    """
    This is a room type representing a planet.
    Planets might have specific features or interactions.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.room_type = "planet"
        self.db.desc = "A distant planet looms ahead, its surface covered in swirling clouds."
        # Add any planet-specific initialization here

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
    