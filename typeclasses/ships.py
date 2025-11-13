import evennia
import string
from evennia import InterruptCommand, utils
import evennia.prototypes
import evennia.prototypes.spawner
from commands.minercommands import MinerCmdSet
import typeclasses
from typeclasses import ship_console, objects, sittables, rooms, exits
from typeclasses.objects import Object
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
    def spawn_ship(ship_class, player):
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

        # ensure the ship has a stable shipID stored on creation
        try:
            if not ship.db.get('shipID'):
                ship.db.shipID = ship.create_ship_id()
        except Exception:
            # ignore if create_ship_id is unavailable
            pass

        # store the pilot as a simple, serializable reference (player key)
        try:
            ship.db.pilot = getattr(player, 'key', str(player))
            # also keep a non-persistent runtime reference for quick lookups
            ship.ndb._pilot_obj = player
            ship.save()
        except Exception:
            # ignore save failures, object will persist via Evennia normally
            pass

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
            create_object(typeclass="typeclasses.exits.Exit", key=exit_to, location=room_objects[exit_from], destination=room_objects[exit_to])



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
        """Transfer all cargo from this ship to destination (merging quantities)."""
        if not self.db.cargo:
            return
        if not hasattr(destination.db, 'cargo') or destination.db.cargo is None:
            destination.db.cargo = {}
        for item, qty in list(self.db.cargo.items()):
            destination.db.cargo[item] = destination.db.cargo.get(item, 0) + qty
        # clear this ship's cargo after transfer
        self.db.cargo = {}

    def warp(self, location):
        room = self.search(location)
        if room:
            self.move_to(room)

    def warp_to_existing_room(self, identifier):
        """
        Warp to a known destination room based on identifier using Evennia search.
        """
        results = search_object(identifier)
        if results:
            destination_room = results[0]
            self.move_to(destination_room)
            self.msg(f"Warping to {destination_room.key}.")
        else:
            self.msg("Destination not found.")

    def target(self, target):
        self.msg(f"Targetting {target}")
        self.db.target = target   

    def display_work_pending(self):
        pilot = self.db.pilot
        if not pilot:
            return
        # if pilot stored as key/string, try to resolve to object
        if isinstance(pilot, str):
            found = search_object(pilot)
            if not found:
                return
            pilot_obj = found[0]
        else:
            pilot_obj = pilot

        contracts = getattr(self.db, 'contracts', None)
        if not contracts:
            pilot_obj.msg("No pending work.")
            return
        active = ContractHandler.list_active_contracts(contracts)
        if not active:
            pilot_obj.msg("No active contracts.")
            return
        for c in active:
            pilot_obj.msg(f"Contract: {c.description} | Reward: {c.reward} | Status: {c.status}")

    def check_cargo(self):
        # return a clean dict of cargo items -> quantities
        return dict(self.db.cargo) if self.db.cargo else {}
    
    #Takes the cargo from the ship's db and deletes it (use when selling or transfering goods)
    def remove_cargo(self, cargo):
        self.db.cargo.pop(cargo, None)



    

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


        self.db.max_orehold = 1000  
        self.db.orehold = 0  
        self.db.credit_value = 50000  

        self.db.health = 100  # Set appropriate initial health
        self.db.shields = 50  # Set appropriate initial shields
        self.db.max_hold = 5000  # Set appropriate max ore hold capacity
        self.db.hold = 0  # Set initial ore hold to 0
        self.db.credit_value = 50000  # Set appropriate credit value

    
    def turn_on(self):
        super().ship_turn_on()
        self.msg("The ground rumbles.")

    def idle(self):
        super().ship_idle()
        self.msg("")

    def start_consoles(self):
        super().start_consoles()
    
    def scan(self):
        if self.db.target:
            asteroid = self.db.target
            resource_contents= asteroid.db.resource_contents
            self.msg(f"Scanning asteroid...")
            self.msg(f"Total resources: {resource_contents}")
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
            
            if self.db.hold + rand > self.db.max_hold:
                self.msg("Your ore hold is full!")
                return

            self.db.hold += rand
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

        self.db.ship_class = "Freighter"

        self.db.max_cargohold = 1000
        self.db.cargohold = 0
        self.db.credit_value = 50000

        self.db.desc = ""
        self.db.health = 0
        self.db.shields = 0

        self.db.hold = 0
        self.db.credit_value = 0

    def turn_on(self):
        super().ship_turn_on()
        self.msg(f"{self.key} roared to life.")

    def idle(self):
        super().ship_idle()
        self.msg(f"{self.key} rumbles noisly.")

    def check_manifest(self):
        """Return a consolidated manifest of cargo currently held."""
        temp_dict = {}
        for item, quantity in (self.db.cargo or {}).items():
            temp_dict[item] = temp_dict.get(item, 0) + quantity
        self.msg(f"Shipping Manifest: {temp_dict}")

    def load_container(self, cargo_container):
        """Attempt to load a cargo container object onto the freighter."""
        size = getattr(cargo_container, 'size', 0)
        if self.db.cargohold + size <= self.db.max_cargohold:
            cargo_container.move_to(self)
            self.db.cargohold += size
            self.msg(f"{cargo_container.key} loaded onto {self.key}.")
        else:
            self.msg(f"Cannot load {cargo_container.key}. Not enough hold capacity.")

    def unload_container(self, cargo_container, weight, location):
        cargo_container.move_to(location)
        self.db.cargohold = max(0, self.db.cargohold - weight)

    def accept_contract(self, contract):
        """Accept a freight contract if space permits and load its cargo into self.db.cargo."""
        total_cargo_volume = sum(contract.cargo.values()) if contract.cargo else 0
        if self.db.cargohold + total_cargo_volume > self.db.max_cargohold:
            self.msg("Not enough cargo space to accept the contract.")
            return False

        # Accept the contract
        accepted = ContractHandler.accept_contract(contract)
        if not accepted:
            self.msg("Failed to accept contract.")
            return False

        # merge cargo into ship
        if not self.db.cargo:
            self.db.cargo = {}
        for item, qty in contract.cargo.items():
            self.db.cargo[item] = self.db.cargo.get(item, 0) + qty
        self.db.cargohold += total_cargo_volume
        self.msg(f"Contract accepted and cargo loaded. Reward: {contract.reward}")
        return True
    


class Researcher(Ships):

    def at_object_creation(self):
        super().at_object_creation()


        self.db.ship_class = "Researcher"
        self.db.max_volatilehold = 1000  
        self.db.volatilehold = 0  
        self.db.credit_value = 50000  

        self.db.desc = ""
        self.db.health = 0
        self.db.sheilds = 0
        self.db.hold = 0
        self.db.max_hold = 500
        self.db.cargo = {}
        self.db.credit_value = 0


    
    def turn_on(self):
        super().ship_turn_on()
        print(f"{self.key} produced random sounds.")

    def idle(self):
        super().ship_idle()
        print(f"{self.key} whirs and clicks randomly.")

    def scan(self):
        if self.db.target:
            anomoly = self.db.target
            point_count = anomoly.db.points
            self.msg(f"Scanning anomoly...")

            if self.db.cargo is None:
                self.db.cargo = {}

            if "research" not in self.db.cargo:
                self.db.cargo["research"] = point_count
            else:
                self.db.cargo["research"] += point_count

            anomoly.delete()
            self.msg(f"{point_count} research points gained!")
        else:
            self.msg("You are not targeting any anomoly.")

    def scan(self):
        if self.db.target:
            anomoly = self.db.target
            point_count = anomoly.db.points
            self.msg(f"Scanning anomoly...")

            if self.db.cargo is None:
                self.db.cargo = {}

            if "research" not in self.db.cargo:
                self.db.cargo["research"] = point_count
            else:
                self.db.cargo["research"] += point_count

            anomoly.delete()
            self.msg(f"{point_count} research points gained!")
        else:
            self.msg("You are not targeting any anomoly.")


class Fighter(Ships):

    def at_object_creation(self):
        super().at_object_creation()

        self.db.ship_class = "Fighter"
        self.db.health = 150  # Fighters have more durability
        self.db.shields = 100  # Higher shield capacity
        self.db.gunslots = 4  # Can equip multiple weapons
        self.db.ammohold = 500  # Stores ammunition
        self.db.genhold = 250  # Less general cargo capacity


        self.db.desc = ""
        self.db.health = 0
        self.db.sheilds = 0
        self.db.gunslots = 0
        self.db.hold = 0
        self.db.max_hold = 1000


    def turn_on(self):
        print(f"{self.key} turned on quietly.")

    def idle(self):
        super().ship_idle()
        print("A quiet whir fills the air.")