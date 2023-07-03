from typing import Self
import evennia
from evennia import InterruptCommand
import typeclasses
from typeclasses.accounts import Account
#from typeclasses import scripts
from typeclasses import ship_console
from typeclasses import objects, sittables
from typeclasses.objects import Object
from typeclasses import rooms, exits, ships
from typeclasses.rooms import Room
from evennia import Command, CmdSet, create_object, create_script, search_object, EvMenu, EvForm, EvTable, TICKER_HANDLER
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

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(ShipCmdSet())
        self.db.cargo = {}
        self.db.targeting = None
        self.db.interior_desc = "You stand in the decompression chamber of your ship. This is where you can board and disembark your ship at will."
        #creates the 4 rooms attached to the ship (all rooms must move too)
        # Create the rooms


        bridge_room = evennia.prototypes.spawner.spawn("ROOM_BRIDGE")[0]
#       #this doesn't work, it doesn't effect the look command
        bridge_room.db.desc = "You stand at the bridge of your ship. It is only large enough for around three people to comfortably be in. There is a Captain's chair made of soft leather and an older console in front of you."
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
        if looker.location == self:
            return self.db.interior_desc
        else:
            return self.db.exterior_desc
        
    def get_display_name(self, looker=None, **kwargs):
        return super().get_display_name(looker, **kwargs)

    def set_pilot(self, player):
        self.db.pilot = player    

    def ship_turn_on(self):
        print(f"{self.key} turned on.")

    def ship_idle(self):
        print(f"{self.key} is iddling.")

    #This doesn't work
    def delete(self):
        room_names = ["Bridge", "Storage", "Quarters"]
        room_list = list()
        for room_name in room_names:
            room = self.search(room_name, candidates=self.contents)
            if room:
                room_list.append(room)

        for room in room_list:
            room.delete()

        super().delete()

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

    def scan(self, player):
        self.db.scan_results = []
        message =  ""
        for content in self.location.contents:
            self.db.scan_results.append(content)
            message += f"{content} "
        player.msg(message)

    def target(self, target):
        self.db.targeting = target   

    

##Definitions for Miner, Fighter, Freighter, and Researcher
class Miner(Ships):
    """
    This creates a mining class ship
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.ship_class = "Miner"
        self.db.exterior_desc = "Not the best mining ship, but it is the cheapest. WARNING: Basic Space is not responsible for death/damage caused by asteroids."
        self.db.health = 7200
        self.db.sheilds = 2500
        self.db.orehold = 10000
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
        resources = target.db.resource_contents
        print(f"Target Resources: {resources}")
        if resources:
            resource = target.db.resource_contents.popitem()
            #checks if hold is full
            if self.db.orehold == 0:
                self.msg("Your ore hold is full!")
                return
            self.db.orehold -= 1
            #Spawns the resource in the ships contents
            loot = evennia.create_object(typeclass="asteroids.Resource",
                                         key = resource[0])
            loot.quantity = resource[1]
            if loot in self.search("Storage").contents:
                loot.quantity += loot.quantity
            else:
                loot.location = self.search("Storage")
            self.msg(f"You mine {resource} from the asteroid.")
            if not target.db.resource_contents:
                #Removes depleted asteroids
                self.stop_mining()

            else:
                self.msg("The asteroid is empty.")
                self.stop_mining()


    def stop_mining(self):
        script = self.search("mine_script")
        print(script)
        script.delete()

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
    
    def at_object_creation(self):
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
