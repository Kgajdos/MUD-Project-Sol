from typing import Self
import evennia
from evennia import InterruptCommand
import typeclasses
from typeclasses import objects, sittables
from typeclasses.objects import Object
from typeclasses import rooms, exits, ships
from typeclasses.rooms import Room
from evennia import Command, CmdSet, create_object, search_object, EvMenu, EvForm, EvTable
from commands import ships, sittables
from commands.ships import ShipCmdSet


## Ship Class definitions only
class Ships(Object):

    def at_object_creation(self):
        self.cmdset.add_default(ShipCmdSet())
        self.db.interior_desc = "You stand in the decompression chamber of your ship. This is where you can board and disembark your ship at will."
        #creates the 4 rooms attached to the ship (all rooms must move too)
        # Create the rooms
        bridge_room = evennia.prototypes.spawner.spawn("ROOM_BRIDGE")[0]
        bridge_room.location = self
        console = create_object(typeclasses.ships.ShipConsole, key="Console", attributes = [("desc", "The main terminal to the ship's computer. Here is where you can interact with your ship.")])
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


    def ship_turn_on(self):
        print(f"{self.key} turned on.")

    def ship_idle(self):
        print(f"{self.key} is iddling.")

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


#################################################################################################################################################
#######################################                 SHIP CONSOLE CODE  

_SHIP_CONSOLE_DICT = []
   



#Ship console! needs menu to attach
class CmdShipConsole(Command):
    """
    Pulls up the ships console

    Usage:
        console
    """
    key = "console"
    locks = "cmd:not cmdinside()"
    help_category = "Ship"

    def func(self):
        self.obj.start_consoles(self.caller)

class CmdShoot(Command):
    """
    Firing the ships main gun

    Usage:
        shoot <target>

    This will fire your ship's main gun. If no target is given,
    you will shoot into the air.
    """
    key = "shoot"
    locks = "cmd:cmdinside()"
    aliases = ["fire", "fire!"]
    help_category = "Ship"

    def func(self):
        "This does the shooting"

        caller = self.caller
        location = caller.location

        #no argument given, shoot into space
        if not self.args:
            message = "BOOM! The ship fires its gun into space!"
            location.msg_contents(message)
            return
        #We have an argument, search for target
        target = caller.search(self.args.strip())
        if target:
            location.msg_contents(f"BOOM! The ship fires its gun at {target.key}!")

class CmdLaunch(Command):
    """
    Firing the ships rockets

    Usage:
        launch <target>

    This will fire your ships rockets. If no target is given, you will shoot into the air.
    """
    key = "launch"
    locks = "cmd:cmdinside()"
    aliases = ["rocket", "rocket!"]
    help_category = "Ship"

    def func(self):
        caller = self.caller
        location = caller.location

        #No argument, launch into space
        if not self.args:
            message = "KABOOM! The ship fires its rocket into space!"
            location.msg_contents(message)
            return
        #Argument, search target
        target = caller.search(self.args.strip())
        if target:
            location.msg_contents(f"KABOOM! The ship fires its rockets at {target.key}!")

class CmdLoadCargo(Command):
    """
    Loading cargo into the ship

    Usage:
        load <cargo>
    """
    key = "load"
    locks = "cmd:cmdinside()"#Add more locks in by adding a ; inside the string after cmdinside()
    help_category = "Ship"

    def parse(self):
        self.args = self.args.strip()

        if not self.args:
            self.caller.msg("Load what cargo?")
            raise InterruptCommand

        
    def func(self):
        #find item in caller's contents
        item = self.caller.search(self.args, candidates = self.caller.contents)
        if not item:
            #if no item is found
            return
        
        #creates the copy
        cargo_item = item.copy(new_key = item.key)

        #stores the cargo as an object
        self.obj.store_cargo(cargo_item, self.caller)
        item.delete()

class CmdUnloadCargo(Command):
    """
    Unloading cargo off of the ship and into a holding container.

    Usage:
        unload <cargo>
    """
    key = "unload"
    locks = "cmd:cmdinside()"#Add more locks in by adding a ; inside the string after cmdinside()
    help_category = "Ship"

    def parse(self):
        self.args = self.args.strip()

        if not self.args:
            self.caller.msg("Load what?")
            raise InterruptCommand
        
    def func(self):
        cargo = self.caller.search(self.args, candidates=self.obj.contents)
        if not cargo:
            return

        cargo.move_to(self.caller)
        self.caller.msg(f"You move {cargo.key} into your inventory")

class ConsoleCmdSet(CmdSet):
    key = "consolecmdset"

    def at_cmdset_creation(self):
        self.add(CmdShipConsole())
        self.add(CmdLoadCargo())
        self.add(CmdUnloadCargo())
        self.add(CmdShoot())
        self.add(CmdLaunch())

#opens an EvMenu to allow interactions with the ship
def menunode_start(caller):
    menu = caller.ndb._evmenu
    ai = menu.ai
    text = f"Welcome aboard Captain {caller.key}. Enter quit or q to exit."
    #This is where every option for the ship console exists
    options = [{
        "desc": "Help", "goto": "menunode_help"},
        {"desc": "Captain's Log", "goto": "menunode_captains_log"},
        {"desc": "Ship Statistics", "goto": "_ship_stats"
    }]
    return text, options

def menunode_help(caller, raw_string, **kwargs):
    text = """Welcome to your ship! You are accessing your onboard computer system. Here you can check out your ships statistics sheet, as well as cargo currently in storage.
Every ship comes with a Captain's log for your convienence.'"""
        
    options = {
        "key": ("(Back)", "back", "b"),
        "desc": "Back to home screen.",
        "goto": "menunode_start"
    }
    return text, options

###### Ship_stats
def _ship_stats(caller, raw_string, **kwargs):
    menu = caller.ndb._evmenu
    ai = menu.ai
    text = ai.ship_sheet(caller)

    options = {
        "key": ("(Back)", "back", "b"),
        "desc": "Back to home screen.",
        "goto": "menunode_start"
    }
    return text, options

def menunode_captains_logs(caller, raw_string, **kwargs):
    text = "Captain's log"
    options = {"key": "_default", "goto": _captains_log}

    return text, options

## Where the actual journal is stored and accessed
def _captains_log(caller, raw_string, **kwargs):
    

    return "menunode_start"


class ShipConsole(Object):

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(ConsoleCmdSet())
        self.db.desc = "This is the main computer of the ship. Here is where you can access things like your Captain's log, or take a look at your ship stats."

    def start_consoles(self, player):
        menunodes = {
            "menunode_start": menunode_start,
            "_ship_stats": _ship_stats,
            "menunode_help": menunode_help,
            "menunode_captains_logs": menunode_captains_logs
        }
        consolename = self.db.name or "Admin"
        EvMenu(player, menunodes, startnode = "menunode_start",
               consolename = consolename, ai = self, console = self.contents)
        
    def ship_sheet(self,player):
        '''Using the EvForm shipform for creation'''
        ship = self.location.location
        form = EvForm("typeclasses.shipform-1")
        form.map(cells={
            1: ship.key,
            2: player.key,
            3: ship.db.ship_class,
            4: ship.db.ship_id
        })
        table = EvTable("CARGO", border="incols")
        for cargo in self.contents:
            table.add_row(cargo.key)
        
        custom_mapping = {"v&": "v2"}
        form.map(tables={"A": table}, literals = custom_mapping)

        print (str(form))
        return str(form)

    def store_cargo(self, cargo, player):
        cargo.move_to(self)
        player.msg(f"You store {cargo.key} in your ship.")
        #_SHIP_CONSOLE_DICT.append({cargo})#This exists as a potenial solution to allow items to be stored in the console but displayed in the Storage room!
        #The idea is by creating a dict with the cargo key, it can be easily accessed by other parts of the ship