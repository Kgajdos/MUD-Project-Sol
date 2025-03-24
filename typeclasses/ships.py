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
        elif ship_class == "Fighter":
            ship = evennia.prototypes.spawner.spawn("BS_FIGHTER_CRICKET")[0]
        elif ship_class == "Freighter":
            ship = evennia.prototypes.spawner.spawn("BS_FREIGHTER_SMALLHAULER")[0]
        elif ship_class == "Researcher":
            ship = evennia.prototypes.spawner.spawn("BS_RESEARCHER_ASTEROIDDUST")[0]

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
        self.db.shipID = self.create_ship_id()
        self.db.contract = {}

        # Common ship attributes
        self.db.health = 100  
        self.db.shields = 50  
        self.db.cargo = {}  
        self.db.max_hold = 500  # Generic cargo hold for all ships

        if not self.exits:
            self.create_rooms()

    def create_rooms(self):
        room_templates = {
            "Bridge": "You stand at the bridge of your ship. The space is cozy...",
            "Storage": "You stand in the main storage room of your ship...",
            "Quarters": "You stand in your ship's quarters, there is a bed here...",
        }

        room_objects = {}  # Store created rooms

        # Create rooms dynamically
        for room_name, room_desc in room_templates.items():
            room = create_object(rooms.Room, key=room_name, location=self)
            room.db.desc = room_desc
            room_objects[room_name] = room  # Store reference

        # Create exits dynamically
        exits = [
            ("Bridge", "Storage"),
            ("Storage", "Bridge"),
            ("Storage", "Quarters"),
            ("Quarters", "Storage"),
        ]

        for exit_from, exit_to in exits:
            create_object(exits.Exit, key=exit_to, location=room_objects[exit_from], destination=room_objects[exit_to])


    def create_ship_id(self):
        """Generate a unique ship ID"""
        while True:
            ship_id = f"{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}-{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}"
            if not search_object(ship_id):  # Ensure uniqueness
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
        self.db.ship_class = "Miner"
        self.db.max_orehold = 1000  
        self.db.orehold = 0  
        self.db.credit_value = 50000  
    
    def turn_on(self):
        super().ship_turn_on()
        self.msg("A deep rumble shakes the ship as the mining drills run a systems check. The dashboard flickers to life, displaying ore scan data.")

    def idle(self):
        super().ship_idle()
        self.msg("The ship vibrates faintly as the drills stay in standby mode. Occasional status updates blink on the console.")

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
        super().at_object_creation()
        self.db.ship_class = "Freighter"
        self.db.max_cargohold = 1000  
        self.db.cargohold = 0  
        self.db.credit_value = 50000  

    def turn_on(self):
        super().ship_turn_on()
        self.msg("The ship's systems boot up sluggishly, the low hum of cargo stabilizers filling the cabin. Status lights confirm the hull's integrity.")

    def idle(self):
        super().ship_idle()
        self.msg("The engines maintain a soft, steady rhythm. The distant clatter of shifting cargo reminds you of the weight you're carrying.")

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
        self.db.ship_class = "Researcher"
        self.db.max_volatilehold = 1000  
        self.db.volatilehold = 0  
        self.db.credit_value = 50000  
    
    def turn_on(self):
        super().ship_turn_on()
        self.msg("An array of analytical tools power on, screens filling with complex data streams. A faint sterilized scent fills the air as lab instruments calibrate.")

    def idle(self):
        super().ship_idle()
        self.msg("The ship hums with quiet efficiency, sensors sweeping the environment. Occasionally, a robotic arm adjusts a delicate sample.")


class Fighter(Ships):
    """
    Represents a fighter-class ship, designed for combat and tactical maneuvering.

    Attributes:
        health (int): Durability of the ship.
        shields (int): Defensive energy shielding.
        gunslots (int): Number of available weapon slots.
        genhold (int): General cargo capacity.
        ammohold (int): Storage space for ammunition.
    """

    def at_object_creation(self):
        """Initialize fighter ship attributes."""
        super().at_object_creation()
        self.db.ship_class = "Fighter"
        self.db.health = 150  # Fighters have more durability
        self.db.shields = 100  # Higher shield capacity
        self.db.gunslots = 4  # Can equip multiple weapons
        self.db.ammohold = 500  # Stores ammunition
        self.db.genhold = 250  # Less general cargo capacity

    def turn_on(self):
        """Power up the ship."""
        self.msg("The reactor core hums with restrained power. Targeting systems flicker online, displaying potential threats in the area.")

    def idle(self):
        """Set the ship to idle mode."""
        self.msg("The ship idles with a quiet, predatory patience. The targeting HUD occasionally flickers, tracking phantom signals.")

    def fire_weapon(self, target):
        """
        Attack a target with an equipped weapon.

        Args:
            target (Object): The enemy or object being fired at.
        """
        if not target:
            self.msg("You need to target something before firing!")
            return

        if self.db.ammohold <= 0:
            self.msg("Out of ammo!")
            return

        # Deduct ammo and perform attack
        self.db.ammohold -= 10  # Example ammo usage
        target.msg(f"{self.key} fires at you!")
        self.msg(f"You fire at {target.key}!")

        # Placeholder for attack resolution
        damage = random.randint(10, 30)
        target.db.health = max(0, target.db.health - damage)
        self.msg(f"You hit {target.key} for {damage} damage!")

        # Check if the target is destroyed
        if target.db.health <= 0:
            target.msg(f"{target.key} is destroyed!")
            target.delete()
