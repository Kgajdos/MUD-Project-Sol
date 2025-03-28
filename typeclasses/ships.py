import evennia
import string
from evennia import InterruptCommand, utils
import evennia.prototypes
import evennia.prototypes.spawner
from commands.minercommands import MinerCmdSet
import typeclasses
from typeclasses import ship_console
from typeclasses import objects, sittables
from typeclasses.objects import Object
from typeclasses import rooms, exits, ships
from typeclasses.rooms import Room
from evennia import Command, CmdSet, create_object, create_script, search_object, EvMenu, EvForm, EvTable, TICKER_HANDLER, search_script
from commands import sittables
from commands.ships import ShipCmdSet
from evennia.utils.utils import lazy_property
import random
from typeclasses.contract import ContractHandler, ContractBase
from typeclasses.rooms import SpaceRoom

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
            ship = evennia.prototypes.spawner.spawn("BS_MINER_ROCKSKIPPER")[0]
            ship.save()
        elif ship_class == "Fighter":
            ship = evennia.prototypes.spawner.spawn("BS_FIGHTER_CRICKET")[0]
            ship.save()
        elif ship_class == "Freighter":
            ship = evennia.prototypes.spawner.spawn("BS_FREIGHTER_SMALLHAULER")[0]
            ship.save()
        elif ship_class == "Researcher":
            ship = evennia.prototypes.spawner.spawn("BS_RESEARCHER_ASTEROIDDUST")[0]
            ship.save()

        return ship
        

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
        self.locks.add("call:false()")
        self.cmdset.add_default(ShipCmdSet())
        self.db.pilot = None
        self.db.name = ""
        self.db.desc = ""
        self.db.cargo = {}
        self.db.targeting = None
        self.db.shipID = self.create_ship_id()
        self.db.contract = {}
        if not self.exits:
            self.create_rooms()

    def create_rooms(self):
        bridge_room = evennia.prototypes.spawner.spawn("ROOM_BRIDGE")[0]
        bridge_room.location = self
        console = evennia.prototypes.spawner.spawn("CONSOLE")[0]
        console.db.desc =  "The main terminal to the ship's computer. Here is where you can interact with your ship."
        chair = evennia.prototypes.spawner.spawn("BS_CHAIR")[0]
        chair.key = "Captains Chair"
        console.move_to(bridge_room)
        chair.move_to(bridge_room)
        storage_room = evennia.prototypes.spawner.spawn("ROOM_STORAGE")[0]
        quarters_room = evennia.prototypes.spawner.spawn("ROOM_QUARTERS")[0]
        bed = evennia.prototypes.spawner.spawn("BS_BED")[0]
        bed.move_to(quarters_room)
       
        # Create the exits between rooms
        create_object(exits.Exit, key="Bridge", location = self, destination = bridge_room) #from Boarding to Bridge
        create_object(exits.Exit, key="Boarding", location = bridge_room, destination = self) #from Bridge back to Boarding
        create_object(exits.Exit, key="Storage", location = bridge_room, destination = storage_room) #from Bridge to Storage
        create_object(exits.Exit, key="Bridge", location = storage_room, destination = bridge_room) #from Storage back to Bridge
        create_object(exits.Exit, key="Quarters", location = storage_room, destination = quarters_room) #from Bridge to Quarters
        create_object(exits.Exit, key="Bridge", location = quarters_room, destination = bridge_room) #from Quarters back to Bridge

    #has not been tested yet
    def create_ship_id(self):
        """
        Creates a randomized ship id in the form of AA-00-BB-11
        
        Checks against the database to ensure the number is unique.
        """
        letter_set_a = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        letter_set_b = random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        number_set_0 = str(random.randint(10, 99))
        number_set_1 = str(random.randint(10, 99))
        
        ship_id = f"{letter_set_a}-{number_set_0}-{letter_set_b}-{number_set_1}"
        
        # Assuming there is a method to check uniqueness
        # if not self.is_unique(ship_id):
        #     return self.create_ship_id()
        
        return ship_id
            

    def get_display_desc(self, looker, **kwargs):
        """
        Get the description of the ship as it appears to a player.

        Args:
            looker (Object): The object that is looking at this object.

            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: The description of the ship as it appears to a player.
        """
        return self.db.desc
        
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

    def warp_to_existing_room(self, identifier):
        """
        Warp to a known destination room based on identifier.
        """
        try:
            destination_room = SpaceRoom.objects.get(key=identifier)
            self.move_to(destination_room)
            self.msg(f"Warping to {destination_room.key}.")
        except SpaceRoom.DoesNotExist:
            self.msg("Destination not found.")

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

    def display_work_pending(self):
        player = self.db.pilot
        if not player:
            return
        player.msg(ContractBase.get_list(self))


    

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
        self.cmdset.add(MinerCmdSet, persistent=True)
        self.db.ship_class = "Miner"
        self.db.health = 100  # Set appropriate initial health
        self.db.shields = 50  # Set appropriate initial shields
        self.db.max_orehold = 1000  # Set appropriate max ore hold capacity
        self.db.orehold = 0  # Set initial ore hold to 0
        self.db.genhold = 500  # Set appropriate general cargo hold capacity
        self.db.credit_value = 50000  # Set appropriate credit value
    
    def turn_on(self):
        super().ship_turn_on()
        self.msg("The ground rumbles.")

    def idle(self):
        super().ship_idle()
        self.msg("")

    def start_consoles(self):
        super().start_consoles()
    
    def scan_asteroid(self):
        if self.db.target:
            asteroid = self.db.target
            resources = asteroid.db.resources
            resource_count = asteroid.db.resource_count
            self.msg(f"Scanning asteroid...")
            for resource, count in resources.items():
                self.msg(f"{resource}: {count}")
            self.msg(f"Total resources: {resource_count}")
        else:
            self.msg("You are not targeting any asteroid.")

    def start_mining_asteroid(self, target):
        new_script = evennia.create_script(typeclass="typeclasses.scripts.AsteroidMiningScript", obj=self, key="mine_script")

    def mine_asteroid(self, target):
        self.msg("Mining...")
        resources = target.db.resource_contents
        if resources:
            mined = random.choice(list(resources.keys()))
            rand = random.randint(0, resources[mined])  # creates a random number between 0 and the amount of available resources
            
            if self.db.orehold + rand > self.db.max_orehold:
                self.msg("Your ore hold is full!")
                return

            self.db.orehold += rand
            if mined in self.db.cargo:
                self.db.cargo[mined] += rand
            else:
                self.db.cargo[mined] = rand

            target.db.resource_contents[mined] -= rand
            if target.db.resource_contents[mined] <= 0:
                del target.db.resource_contents[mined]

            self.msg(f"You mine {rand} {mined} from the asteroid.")
        
            if not target.db.resource_contents:
                # Removes depleted asteroids
                self.msg("The asteroid is empty.")
                self.stop_mining()
                target.delete()

    def stop_mining(self):
        scripts = self.scripts.get("mine_script")
        if scripts:
            for script in scripts:
                script.stop()
            self.msg("You stop mining.")
        else:
            self.msg("No mining script found.")

class Freighter(Ships):
    """
    Represents a freighter ship in the game.

    Attributes:
        exterior_desc (str): Description of the freighter's exterior, including a warning about slow travel.
        health (int): The health points of the freighter, indicating its durability.
        shields (int): The shield points of the freighter, providing additional protection.
        hold (int): The cargo hold capacity of the freighter.
        credit_value (int): The value of the freighter in credits.

    Methods:
        at_object_creation(): Initializes the freighter's attributes when it is first created.
        turn_on(): Turns on the freighter's systems.
        idle(): Sets the freighter to idle mode.
        check_manifest(): Generates and displays a shipping manifest for the cargo container.
        load_container(cargo_container): Loads a cargo container onto the freighter.
        unload_container(cargo_container, weight, location): Unloads a cargo container from the freighter.
        accept_contract(contract): Accepts a freight contract and loads the cargo onto the freighter.
    """
    def at_object_creation(self):
        """
        Called when the freighter object is first created. Initializes its attributes.

        Notes:
            - Calls the at_object_creation method of the base class (Ships) to set up common ship attributes.
            - Sets the exterior description, health, shields, fragilehold, genhold, and credit_value attributes.
        """
        super().at_object_creation()
        self.db.desc = ""
        self.db.health = 0
        self.db.shields = 0
        self.db.hold = 0
        self.db.credit_value = 0 

    def turn_on(self):
        super().ship_turn_on()
        self.caller.msg(f"{self.key} roared to life.")

    def idle(self):
        super().ship_idle()
        self.caller.msg(f"{self.key} rumbles noisly.")

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
        if self.db.hold - cargo_container.size >= 0:
            cargo_container.move_to(self)
            self.db.hold -= cargo_container.size
            self.caller.msg(f"{cargo_container.key} loaded onto {self.key}.")
        else:
            self.caller.msg(f"Cannot load {cargo_container.key}. Not enough hold capacity.")

    def unload_container(self, cargo_container, weight, location):
        cargo_container.move_to(location)
        self.db.hold += weight
        

    def accept_contract(self, contract):
        """
        Accepts a freight contract and loads the cargo onto the freighter.

        Args:
            contract (FreightContract): The freight contract to accept.

        Returns:
            bool: True if the contract is successfully accepted and cargo loaded, False otherwise.
        """
        # Check if the contract cargo can fit within the available cargo space
        total_cargo_volume = sum(contract.cargo.values())
        if self.db.hold - total_cargo_volume < 0:
            self.caller.msg("Not enough cargo space to accept the contract.")
            return False

        # Attempt to accept the contract
        result = ContractHandler.accept_contract(contract)
        self.caller.msg(result)
        return True
    


class Researcher(Ships):

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = ""
        self.db.health = 0
        self.db.sheilds = 0
        self.db.voltilehold = 0
        self.db.genhold = 0
        self.db.credit_value = 0
    
    def turn_on(self):
        super().ship_turn_on()
        print(f"{self.key} produced random sounds.")

    def idle(self):
        super().ship_idle()
        print(f"{self.key} whirs and clicks randomly.")


class Fighter(Ships):

    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = ""
        self.db.health = 0
        self.db.sheilds = 0
        self.db.gunslots = 0
        self.db.genhold = 0
        self.db.ammohold = 0

    def turn_on(self):
        print(f"{self.key} turned on quietly.")

    def idle(self):
        super().ship_idle()
        print("A quiet whir fills the air.")