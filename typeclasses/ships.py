import evennia
from evennia import InterruptCommand, utils
from commands.minercommands import MinerCmdSet
import typeclasses
from typeclasses.accounts import Account
from typeclasses import ship_console
from typeclasses import objects, sittables
from typeclasses.objects import Object
from typeclasses import rooms, exits, ships
from typeclasses.rooms import Room
from evennia import Command, CmdSet, create_object, create_script, search_object, EvMenu, EvForm, EvTable, TICKER_HANDLER, search_script
from commands import sittables
from commands.ships import ShipCmdSet
import random

#exists as a way to spawn ships in for the player
class ShipManager:
    @staticmethod
    def spawn_ship(ship_class):
        """
        Spawn a new ship of the given ship class.

        Args:
            ship_class (str): The ship/player class.

        Returns:
            obj: The spawned ship object.
        """
        ship = None
        if ship_class == "Miner":
            ship = Miner()
        elif ship_class == "Fighter":
            ship = Fighter()
        elif ship_class == "Freighter":
            ship = Freighter()
        elif ship_class == "Researcher":
            ship = Researcher()

        if ship:
            ship.setup_rooms()
            ship.setup_exits()
            return ship

        return None
        

## Ship Class definitions only
class Ships(Object):
    """
    This is the Ships class. Ships are objects that players can use to travel through space.

    Attributes:
        cargo (dict): A dictionary mapping cargo names to their quantities.
        targeting (Object): The object that the ship is currently targeting.
        interior_desc (str): The description of the interior of the ship.
        exterior_desc (str): The description of the exterior of the ship.

    Methods:
        at_object_creation(): Set up the ship when it is created.
        get_display_desc(looker, **kwargs): Get the description of the ship as it appears to a player.
        get_display_name(looker=None, **kwargs): Get the name of the ship as it appears to a player.
        set_pilot(player): Set the pilot of the ship.
        ship_turn_on(): Turn on the ship.
        ship_idle(): Put the ship in idle mode.
        delete(): Delete the ship and all its rooms.
        warp_to_space(): Warp the ship into space.
        scan(player, target): Scan a target for resources.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(ShipCmdSet())
        self.db.cargo = {}
        self.db.targeting = None
        self.db.interior_desc = "You stand in the decompression chamber of your ship. This is where you can board and disembark your ship at will."
        bridge = self.search("Bridge")
        if not bridge:
            self.create_rooms()

    def create_rooms(self):
        bridge_room = evennia.prototypes.spawner.spawn("ROOM_BRIDGE")[0]
#       #this doesn't work, it doesn't effect the look command
        bridge_room.db.desc = "You stand at the bridge of your ship. The space is cozy and intimate, with room for only three people to comfortably stand. A soft leather Captain's chair sits in front of you, and an older console hums quietly in the background."
        bridge_room.location = self
        console = create_object(typeclasses.ship_console.ShipConsole, key="Console", location = self, attributes = [("desc", "The main terminal to the ship's computer. Here is where you can interact with your ship.")])
        chair = create_object(typeclasses.sittables.Sittable, key = "Captain's Chair", attributes = [("desc", "A soft leather chair.")])
        console.move_to(bridge_room)
        chair.move_to(bridge_room)
        storage_room = create_object(rooms.Room, key = "Storage", location = self, attributes = [("desc", "You stand in the main storage room of your ship, there is space here for plenty of cargo.")])
        quarters_room = create_object(rooms.Room, key = "Quarters", location = self, attributes = [("desc", "You stand in your ship's quarters, there is a bed here for you to sleep in.")])

       
        # Create the exits between rooms
        create_object(exits.Exit, key="Bridge", location = self, destination = bridge_room) #from Boarding to Bridge
        create_object(exits.Exit, key="Boarding", location = bridge_room, destination = self) #from Bridge back to Boarding
        create_object(exits.Exit, key="Storage", location = bridge_room, destination = storage_room) #from Bridge to Storage
        create_object(exits.Exit, key="Bridge", location = storage_room, destination = bridge_room) #from Storage back to Bridge
        create_object(exits.Exit, key="Quarters", location = storage_room, destination = quarters_room) #from Bridge to Quarters
        create_object(exits.Exit, key="Bridge", location = quarters_room, destination = bridge_room) #from Quarters back to Bridge

    def get_display_desc(self, looker, **kwargs):
        """
        Get the description of the ship as it appears to a player.

        Args:
            looker (Object): The object that is looking at this object.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: The description of the ship as it appears to a player.
        """
        if looker.location == self:
            return self.db.interior_desc
        else:
            return self.db.exterior_desc
        
    def get_display_name(self, looker=None, **kwargs):
        """
         Get the name of the ship as it appears to a player.

         Args:
             looker (Object): The object that is looking at this object.

             **kwargs: Arbitrary keyword arguments.

         Returns:
             str: The name of the ship as it appears to a player.
         """
        return super().get_display_name(looker, **kwargs)

    def set_pilot(self, player):
        """
         Set the pilot of the ship.

         Args:
             player (Object): The object that will be piloting this ship.
        """
        self.db.pilot = player    

    def ship_turn_on(self):
        print(f"{self.key} turned on.")

    def ship_idle(self):
        print(f"{self.key} is iddling.")
    
    def store_cargo(self, destination):
        if self.db.cargo:
            for items in self.db.cargo.items():
                destination.db.cargo += items

    def warp(self, location):
        room = self.search(location)
        self.move_to(room)

    def warp_to_space(self):
        """
        Warp the ship into space.

        Returns:
            bool: True if the ship successfully warps into space, False otherwise.
        """
        #dict of available rooms
        rooms = {("#161", "#187", "#189", "#195", "#201", "#208", "#213", "#219", "#224")}
        # Check if the ship is already in space
        if self.location == "space":
            return False
        
        # Check if the ship is in a valid location to warp from (e.g., a hangar)
        if not self.location.is_hangar:
            return False

        # Move the ship to the space location
        space = random.choice(rooms)
        self.move_to(space)
        return True

    def scan(self, player, target):
        self.db.scan_results = []
        message = ""
        if hasattr(target.db, "resource_contents"):
            for content in target.db.resource_contents:
                self.db.scan_results.append(content)
                message += f"{content} "
        else:
            message = "No resource contents found."
        player.msg(message)

    def target(self, target):
        self.msg(f"Targetting {target}")
        self.db.target = target   

                


    

##Definitions for Miner, Fighter, Freighter, and Researcher
class Miner(Ships):
    """
    This creates a mining class ship

    Attributes:
        ship_class (str): The class of the ship.
        exterior_desc (str): The description of the exterior of the ship.
        health (int): The health of the ship.
        shields (int): The shields of the ship.
        orehold (int): The amount of ore that the ship can hold.
        genhold (int): The amount of general cargo that the ship can hold.
        credit_value (int): The value of the ship in credits.

    Methods:
        at_object_creation(): Set up the miner when it is created.
        turn_on(): Turn on the miner.
        idle(): Put the miner in idle mode.
        start_consoles(): Start the consoles on the miner.
        scan_asteroid(): Scan an asteroid for resources.
        start_mining_asteroid(target): Start mining an asteroid.
        mine_asteroid(target): Mine an asteroid for resources.
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add(MinerCmdSet, persistent = True)
        self.db.ship_class = "Miner"
        self.db.exterior_desc = "Not the best mining ship, but it is the cheapest. WARNING: Basic Space is not responsible for death/damage caused by asteroids."
        self.db.health = 7200
        self.db.sheilds = 2500
        self.db.max_orehold = 1500
        self.db.orehold = 1500
        self.db.genhold = 50
        self.db.credit_value = 15000
    
    def turn_on(self):
        super().ship_turn_on()
        print("The ground rumbles.")

    def idle(self):
        super().ship_idle()
        print("")

    def start_consoles(self):
        super().start_consoles()
    
    def scan_asteroid(self):
        if self.db.target:
            asteroid = self.db.target
            resources = asteroid.db.resources
            resource_count = asteroid.db.resource_count
            self.msg(f"Scanning asteroid...")
            for resource, count in resources.items():
                self.msg("f{resource}: {count}")
            self.msg(f"Total resources: {resource_count}")
        else:
            self.msg("You are not targetting any asteroid.")

    #Basic mining function, not very interesting....
    def start_mining_asteroid(self, target):
        new_script = evennia.create_script(typeclass = "typeclasses.scripts.AsteroidMiningScript", obj = self, key = "mine_script")


    def mine_asteroid(self, target):
        self.msg("Mining...")
        resources = target.db.resource_contents
        if resources:
            mined = random.choice(list(resources))
            rand = random.randint(0,resources[mined]) #creates a random number between 0 and the amount of available resources
            print(rand)
            if self.db.orehold <= 0:
                self.msg("Your ore hold is full!")
                return
            self.db.orehold -= rand
            if mined in self.db.cargo:
                self.db.cargo[mined] += rand
                target.db.resource_contents[mined] -= rand
                if target.db.resource_contents[mined] <= 0:
                    target.db.resource_contents.pop(mined)
            else:
                self.db.cargo[mined] = rand
                if target.db.resource_contents[mined] <= 0:
                    target.db.resource_contents.pop(mined)
            self.msg(f"You mine {rand} {mined} from the asteroid.")
        if not target.db.resource_contents:
                #Removes depleted asteroids
            self.msg("The asteroid is empty.")
            self.stop_mining()
            target.delete()



    def stop_mining(self):
        script = self.scripts.get("mine_script")
        if script:
            script[0].stop()
            self.msg("You stop mining.")

class Fighter(Ships):


    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.exterior_desc = "The Basic Space line has served as a low cost entry to space combat for generations. WARNING: Basic Space is not responisble for death of a pilot in the event of a firefight."
        self.db.health = 1300
        self.db.sheilds = 3500
        self.db.ammohold = 100
        self.db.genhold = 50
        self.db.credit_value = 15000


    def ship_define_stats(self, size, health, shields, speed, no_of_rooms):
        super().ship_define_stats(size, health, shields, speed, no_of_rooms)
    
    def turn_on(self):
        print(f"{self.key} turned on quietly.")

    def idle(self):
        super().ship_idle()
        print("A quiet whir fills the air.")


class Freighter(Ships):
    """
    Represents a freighter ship in the game.

    Attributes:
        exterior_desc (str): Description of the freighter's exterior, including a warning about slow travel.
        health (int): The health points of the freighter, indicating its durability.
        shields (int): The shield points of the freighter, providing additional protection.
        fragilehold (int): The fragile hold capacity of the freighter, representing its sensitivity to certain cargos.
        genhold (int): The general cargo hold capacity of the freighter.
        credit_value (int): The value of the freighter in credits.

    Methods:
        at_object_creation(): Called when the freighter object is first created, initializes its attributes.
        turn_on(): Turns on the freighter's systems, calling the base class method and displaying a message.
        idle(): Sets the freighter to idle mode, calling the base class method and displaying a message.
        load_container(cargo_container): Loads a cargo container onto the freighter.
    """
    def at_object_creation(self):
        """
        Called when the freighter object is first created. Initializes its attributes.

        Notes:
            - Calls the at_object_creation method of the base class (Ships) to set up common ship attributes.
            - Sets the exterior description, health, shields, fragilehold, genhold, and credit_value attributes.
        """
        super().at_object_creation()
        self.db.exterior_desc = "Basic Space has created a luxurious tank, so you ran rest well knowing the pirates wont even leave a scratch! WARNING: Basic Space is not responsible for any hardship as a result of slow travel."
        self.db.health = 5700
        self.db.sheilds = 10000
        self.db.fragilehold = 100
        self.db.genhold = 1000
        self.db.credit_value = 15000    

    def turn_on(self):
        super().ship_turn_on()
        print(f"{self.key} roared to life.")

    def idle(self):
        super().ship_idle()
        print(f"{self.key} rumbles noisly.")

    def check_manifest(self):
        """
        Generates and displays a shipping manifest for the cargo container.

        Notes:
            - The method iterates through the cargo container's contents and consolidates the quantities of each item.
            - The resulting shipping manifest is displayed to the caller.
        """
        temp_dict = {}
        for item, quantity in self.db.contents.items():
            temp_dict[item] += quantity
        self.msg(f"Shipping Manifest: {temp_dict}")

    def load_container(self, cargo_container):
        """
        Loads a cargo container onto the freighter.

        Args:
            cargo_container (Object): The cargo container to be loaded.

        Notes:
            - Moves the cargo container to the freighter's location.
            - Assumes that the cargo container is compatible with the freighter's hold capacity.
            - If the freighter's hold capacity is exceeded, the cargo container will not be loaded.
        """
        if self.db.general_hold_capacity - cargo_container.size >= 0:
            cargo_container.move_to(self)
            self.db.general_hold_capacity -= cargo_container.size
            print(f"{cargo_container.key} loaded onto {self.key}.")
        else:
            print(f"Cannot load {cargo_container.key}. Not enough hold capacity.")

    def unload_container(self, cargo_container, location):
        cargo_container.move_to(location)
    


class Researcher(Ships):

    def at_object_creation(self):
        super().at_object_creation()
        self.db.exterior_desc = "Let Basic Space take you to the corners of the galaxy. WARNING: Basic Space is not responsible for loss of life due to strandenment."
        self.db.health = 1000
        self.db.sheilds = 5000
        self.db.voltilehold = 50
        self.db.genhold = 500
        self.db.credit_value = 15000
    
    def turn_on(self):
        super().ship_turn_on()
        print(f"{self.key} produced random sounds.")

    def idle(self):
        super().ship_idle()
        print(f"{self.key} whirs and clicks randomly.")
