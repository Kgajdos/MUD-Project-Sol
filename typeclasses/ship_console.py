import datetime
import time
from evennia import utils
from evennia.utils import delay
from typeclasses import ships
from typeclasses.objects import Object
from evennia import InterruptCommand
from evennia import Command, CmdSet, create_object, search_object, EvMenu, EvForm, EvTable
from typeclasses.rooms import SpaceRoom

#******Logic for space exploration, likely will need to be refractored and moved******
def get_all_space_rooms():
    """
    Retrieve all SpaceRoom instances.
    
    Returns:
        QuerySet: A Django QuerySet of all SpaceRoom objects.
    """
    return SpaceRoom.objects.all()

def get_all_specific_rooms(room_type):
    """
    Retrieve all instances of a specific type of SpaceRoom.
    
    Args:
        room_type (str): The type of room to filter by (e.g., 'AsteroidRoom').
    
    Returns:
        QuerySet: A Django QuerySet of rooms of the specified type.
    """
    return SpaceRoom.objects.filter(db_typeclass_path=f'typeclasses.rooms.{room_type}')

def print_room_details():
    """
    Print details of all SpaceRoom instances.
    """
    rooms = get_all_space_rooms()
    for room in rooms:
        print(f"Room Name: {room.key}, Type: {room.db_typeclass_path}")

def get_room_by_name(name):
    """
    Retrieve a SpaceRoom instance by its name.
    
    Args:
        name (str): The name of the room to retrieve.
    
    Returns:
        SpaceRoom: The room instance if found, or None if not.
    """
    try:
        return SpaceRoom.objects.get(db_key=name)
    except SpaceRoom.DoesNotExist:
        print(f"Room with name {name} does not exist.")
        return None


def get_all_space_room_identifiers():
    """
    Retrieve all unique identifiers for space rooms.
    """
    # Use the correct field name
    identifiers = SpaceRoom.objects.values_list('db_key', flat=True).distinct()
    return list(identifiers)




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

    def at_pre_cmd(self):
        #this function will terminate the command if this function returns True. 
        if not self:
            ship = self.obj.location.location
            if ship.db.pilot != self.caller.key:
                self.caller.msg("You are not authorized to access this console!")
                raise InterruptCommand

    def func(self):
        self.obj.start_consoles(self.caller, self.session)


class CmdWarp(Command):
    """
    Initiates a warp to a random sector in space.

    Usage:
        warp

    This command warps the spaceship to a random sector in space.
    """
    key = "warp"
    locks = "cmd:cmdinside()"
    help_category = "Ship"

    def parse(self):
        # Code for warping the spaceship to a random sector in space
        # ...
        pass


    def func(self):
        # Code for launching the spaceship into space
        # ...
        self.obj.warp_to_space()

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
    locks = "cmd:cmdinside()"
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
        self.add(CmdWarp())
###########################################################################################################

#opens an EvMenu to allow interactions with the ship
def menunode_start(caller):
    """
    This is the start of the ship console's menu. Any additions to this menu must be added here.

    --menunode_help
            All relevant help for the ship, this can be where the player is reminded how to load and unload, alongside combat.
    --menunode_captains_logs
            A menunode strictly for the player to have an in game journal.
    --_ship_stats
            A non-interactive page for viewing the ship's statistics in a visual way.
    """
    menu = caller.ndb._evmenu
    ai = menu.ai
    text = f"Welcome aboard Captain {caller.key}. Enter quit or q to exit."
    #This is where every option for the ship console exists
    options = [{
        "desc": f"|gHelp|n", "goto": "menunode_help"},
        {"desc": f"|gCaptain's Log|n", "goto": "menunode_captains_logs"},
        {"desc": f"|gShip Statistics|n", "goto": "_ship_stats"},
        {"desc": f"|gFly Ship|n", "goto": "menunode_fly_ship"},
        {"desc": f"|cSet Destination|n", "goto": "menunode_set_destination"},
        {"desc": f"|cChart New Course|n", "goto": "menunode_chart_course"},
        {"desc": f"|cRename Ship|n", "goto": "menunode_ship_rename"}
        ]
    return text, options

def menunode_help(caller, raw_string, **kwargs):
    text = f"""Welcome to your ship! You are accessing your onboard computer system. Here you can check out your ships statistics sheet, as well as cargo currently in storage.
Every ship comes with a Captain's log for your convienence.

To make things simpler, your options are color coded:
|cCyan|n: This means you are about to interact with or modify your ship. (example: new Captain's log.)
|gGreen|n: This means you are recieving information about your ship.
|yYellow|n: This refers to basic screen options."""
        
    options = {
        "key": (f"|y(Back)|n", "back", "b"),
        "desc": "Back to home screen.",
        "goto": "menunode_start"
    }
    return text, options

def menunode_captains_logs(caller, raw_string, **kwargs):
    menu = caller.ndb._evmenu
    player = menu.caller
    text = f"""Welcome {player.key}. Choose log to read, or start a new log."""

    options = [{
        "key": (f"|c(New)|n", "new", "n"),
        "desc": "Create new log.",
        "goto": "menunode_new_log" 
    },{
        "key": (f"|g(Read)|n", "read", "r"),
        "desc": "Read old logs.",
        "goto": "menunode_choose_log"
    },
    {
        "key": (f"|y(Back)|n", "back", "b"),
        "desc": "Back to home screen.",
        "goto": "menunode_start"
    }]
    return text, options

###### Ship_stats
def _ship_stats(caller, raw_string, **kwargs):
    menu = caller.ndb._evmenu
    ai = menu.ai
    text = ai.ship_sheet(caller)

    options = {
        "key": (f"|y(Back)|n", "back", "b"),
        "desc": "Back to home screen.",
        "goto": "menunode_start"
    }
    return text, options

def menunode_new_log(caller, raw_string, **kwargs):
    """
    Create a new log.
    """
    text = f"""Begin typing up log, press enter to save log to console. 
Remember that for the time being, all logs are |rpermanent|n!"""

    options = {"key": "_default", "goto": _new_log}

    return text, options

def _new_log(caller, raw_string, **kwargs):
    #menu = caller.ndb._evmenu
    #player = menu.caller
    new_entry = raw_string
    log_date = datetime.datetime.now()
    years_added = log_date.year + 2053
    date = log_date.strftime("%Y-%m-%d")
    date_2 = log_date.replace(year = years_added).strftime("%Y-%m-%d")
    if not caller.db.logs:
        caller.db.logs = {}
    if not caller.db.logs.get(date):
        caller.db.logs[date] = new_entry
    else:
        caller.db.logs[date] += new_entry

    return "menunode_captains_logs"

def menunode_choose_log(caller, raw_string, **kwargs):
    text = "Choose a Date."
    options = []

    for date, data in caller.db.logs.items():
        options.append({"desc": (f"|g{date}|n"),
                        "goto": ("menunode_read_log", {"date": date})})

    return text, options

def menonode_read_log(caller, raw_string, **kwargs):
    date = kwargs.get('date')
    text = caller.db.logs[date]
    options = {
        "key": (f"|y(Back)|n", "back", "b"),
        "desc": "Back to home screen.",
        "goto": "menunode_start"
    }
    return text, options

def menunode_store_cargo(caller, raw_string, **kwargs):
    text = f"Store cargo in your "

def menunode_ship_rename(caller, raw_string, **kwargs):
    text = f"""Type in a new name for your ship and press enter. 
|rWARNING: You will not be notified of this change!|n"""

    options = {"key": "_default", "goto": _new_name}

    return text, options

def _new_name(caller, raw_string, **kwargs):
    menu = caller.ndb._evmenu
    menu.ai.set_new_name(caller, raw_string)

    return "menunode_start"

def menunode_confirm_travel(caller, raw_string, **kwargs):
    """
    Confirm the travel to the chosen destination.
    """
    destination = kwargs.get("destination")
    caller.msg(f"Debug: Destination is {destination}")

    if not destination:
        caller.msg("Invalid destination.")
        return "menunode_set_destination"
    
    ship = caller.location.location
    caller.msg(f"Debug: Ship is {ship}")

    if not ship:
        caller.msg("You are not on a ship.")
        return "menunode_set_destination"

    try:
        destination_room = SpaceRoom.objects.get(db_key=destination)
        caller.msg(f"Debug: Destination room found with key {destination_room.db_key}")
    except SpaceRoom.DoesNotExist:
        caller.msg("Destination not found.")
        return "menunode_set_destination"
    except SpaceRoom.MultipleObjectsReturned:
        caller.msg("Multiple destinations found, something went wrong.")
        return "menunode_set_destination"

    ship.move_to(destination_room)
    caller.msg(f"The ship is now traveling to {destination_room.key}.")

    return "menunode_start"


def menunode_travel(caller, raw_string, **kwargs):
    """
    Move the ship to the selected room.
    """
    destination_room = kwargs.get("destination_room")

    if not destination_room:
        caller.msg("An error occurred: destination room not found.")
        return "menunode_set_destination"

    # Assuming the player is on the ship's bridge and the ship is the location of the bridge's location
    ship = caller.location.location

    if not ship:
        caller.msg("An error occurred: ship not found.")
        return "menunode_start"

    # Check if the destination room exists
    if not SpaceRoom.objects.filter(key=destination_room.key).exists():
        caller.msg("An error occurred: destination room does not exist.")
        return "menunode_set_destination"

    # Move the ship to the destination room
    ship.msg_contents(f"The ship is now traveling to {destination_room.key}...")
    ship.location = destination_room
    ship.save()

    # Notify the caller that the ship has arrived
    caller.msg(f"The ship has arrived at {destination_room.key}.")

    return "menunode_start"



# Constants for pagination
OPTIONS_PER_PAGE = 20

def get_paginated_options(options, page):
    """
    Paginate the options for display.
    
    :param options: List of all options.
    :param page: Current page number (1-based index).
    :return: Paginated options for the current page.
    """
    start_index = (page - 1) * OPTIONS_PER_PAGE
    end_index = start_index + OPTIONS_PER_PAGE
    return options[start_index:end_index]

def menunode_set_destination(caller, raw_string):
    """
    Set the ship's destination based on the user's input.
    """
    destination = raw_string.strip()  # Clean up the input
    print(f"Debug: Destination is {destination}")
    
    # Retrieve all space room identifiers
    identifiers = get_all_space_room_identifiers()
    print(f"Debug: Available identifiers are {identifiers}")

    if destination not in identifiers:
        print(f"Destination not found: {destination}")
        caller.msg("The destination could not be found.")
        return

    # Proceed with setting the destination
    caller.msg(f"Destination {destination} is set.")


def menunode_chart_course(caller, raw_string, **kwargs):
    """
    Menu node for charting a new course.
    """
    from typeclasses.rooms import create_new_room
    new_room = create_new_room()  # Create a new room with a random type and description
    # Provide a description of the action to the player
    text = f"You have charted a new course to {new_room.key}. Do you want to proceed?"
    
    # Define the options for the player
    options = [
        {"desc": "Yes, confirm travel", "goto": ("menunode_confirm_travel", {"destination": new_room.db_key})},
        {"desc": "No, choose another destination", "goto": "menunode_set_destination"}
    ]
    
    # Return the text and options for the menu
    return text, options
def menunode_fly_ship(caller, raw_string, **kwargs):
    text = f"Begin flying your ship?"

    options = [
        {"key": "|gYes|n", "goto": _puppet},
        {"key": "|yNo|n", "goto": "menunode_start"}
        ]
    return text, options

def _puppet(caller, raw_string, **kwargs):
    caller.msg("Attempting to connect neurocybernetics to Ship.")
    ship = caller.location.location
    session = caller.ndb._evmenu._session
    account = session.account
    account.puppet_object(session, ship)
    return "menunode_end"

def menunode_end(caller, raw_string, **kwargs):
    return None

def create_unique_identifier(base_identifier):
    """
    Generate a unique identifier for a new room.
    """
    existing_identifiers = get_all_space_room_identifiers()
    new_identifier = base_identifier
    counter = 1
    while new_identifier in existing_identifiers:
        new_identifier = f"{base_identifier}_{counter}"
        counter += 1
    return new_identifier



class ShipConsole(Object):

    def at_object_creation(self):
        """
            Called when the object is created. Adds default console commands and initializes object properties.

            Notes:
                - This method is automatically called by Evennia during object creation.

        """
        super().at_object_creation()
        self.cmdset.add_default(ConsoleCmdSet())
        self.db.desc = "This is the main computer of the ship. Here is where you can access things like your Captain's log, or take a look at your ship stats."
        self.db.logs = []

    def start_consoles(self, player, session):
        """
        Start the ship console's main menu.

        Args:
            player (Player): The player using the console.
            session (Session): The session through which the player is interacting.

        """
        menunodes = {
            "menunode_start": menunode_start,
            "_ship_stats": _ship_stats,
            "menunode_help": menunode_help,
            "menunode_captains_logs": menunode_captains_logs,
            "menunode_new_log": menunode_new_log,
            "menunode_choose_log": menunode_choose_log,
            "menunode_read_log": menonode_read_log,
            "menunode_ship_rename": menunode_ship_rename,
            "menunode_fly_ship": menunode_fly_ship,
            "menunode_end": menunode_end,
            "menunode_confirm_travel": menunode_confirm_travel,
            "menunode_travel": menunode_travel,
            "menunode_set_destination": menunode_set_destination, 
            "menunode_chart_course": menunode_chart_course 
        }
        consolename = self.db.name or "Admin"
        EvMenu(player, menunodes, startnode = "menunode_start",
               consolename = consolename, ai = self, console = self.contents, session = session)
        
    def set_new_name(self, player, new_name):
        """
        Set a new name for the ship.

        Args:
            player (Player): The player who is renaming the ship.
            new_name (str): The new name for the ship.

        """
        ship = player.db.active_ship
        ship.key = new_name

    def ship_sheet(self,player):
        """
        Generate and return the ship's information as an EvForm for creation.

        Args:
            player (Player): The player requesting the ship information.

        Returns:
            str: The ship's information as an EvForm.

        """
        ship = self.location.location
        form = EvForm("typeclasses.shipform-1")
        form.map(cells={
            1: ship.key,
            2: ship.db.pilot,
            3: ship.db.ship_class,
            4: ship.db.shipID
        })
        table = EvTable("CARGO", border="incols")
        storage = ship.db.cargo
        print(storage)
        if not storage:
            table.add_row("No cargo")
        else:
            for i, (cargo, quantity) in enumerate(storage.items()):
                if i == 8 and len(storage) > 10:
                    table.add_row("etc...")
                    break
                table.add_row(f"{cargo}: {quantity}")       
        custom_mapping = {"v&": "v2"}
        form.map(tables={"A": table}, literals = custom_mapping)

        return str(form)

