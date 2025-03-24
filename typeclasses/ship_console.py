import datetime
import time
from evennia import utils
from evennia.utils import delay
from typeclasses import ships
from typeclasses.objects import Object
from evennia import InterruptCommand
from evennia import Command, CmdSet, create_object, search_object, EvMenu, EvForm, EvTable
from typeclasses.rooms import SpaceRoom
from evennia import logger

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
    identifiers = utils.search.search_typeclass(SpaceRoom, include_children = True)
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
        if not self.obj:
            self.obj = self.caller.location

        ship = self.obj.location.location

        if str(ship.db.pilot) != str(self.caller.key):
            self.caller.msg("You are not authorized to access this console!")
            raise InterruptCommand

    def func(self):
        if not self.obj:
            self.caller.mg("No console available to interact with")
            return
        
        if hasattr(self.obj, 'start_consoles'):
            self.obj.start_consoles(self.caller, self.session)
        else:
            self.caller.msg("The console is malfunctioning.")


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


def menunode_confirm_travel(caller, *raw_string, **kwargs):
    """
    Confirm the player's choice to travel to the selected destination.
    """
    destination = str(kwargs['destination']).strip()
    menu_text = f"You've selected {destination}. Do you want to proceed with this destination?"

    caller.db.travel_destination = destination

    choices = {
        "key": (f"Yes"),
        "desc": f"Confirm Travel",
        "goto": "menunode_travel"
    }

    return menu_text, choices


def menunode_travel(caller):
    """
    Move the ship to the selected room.
    """
    destination_name = caller.db.travel_destination
    destination_room = search_object(destination_name)

    print(f"Destination room: {destination_room}")
    print(f"Destination name: {destination_name}")

    if not destination_room:
        caller.msg("Error: Room not found!")
        return 
    
    ship = caller.location.location

    ship.move_to(destination_room[0])
    caller.msg(f"You travel to {destination_name}")

    return 



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

def menunode_set_destination(caller, raw_string, page = 1):
    """
    Set the ship's destination based on the user's input.
    """
    identifiers = get_all_space_room_identifiers()

    paginated_options = get_paginated_options(identifiers, page)

    if not paginated_options:
        caller.msg("No destinations available")
        return
    

    total_pages = (len(identifiers) + OPTIONS_PER_PAGE - 1) // OPTIONS_PER_PAGE

    option_text = "\n".join([f"{index + 1}.{destination}" for index, destination in enumerate(paginated_options)])
    menu_text = f"Choose your destination:\n{option_text}\n"
    
    if page > 1:
        menu_text += "Press [N] for next page."
    if page < total_pages:
        menu_text += "Press [P] for previous page."
    
    menu_text += f"Page{page} of {total_pages}"

    choices = []

    if page > 1:
        choices.append({
            "key": "P",
            "callback": ("menunode_set_destination", page - 1)
        })

    if page < total_pages:
        choices.append({
            "key": "N",
            "callback": ("menunode_set_destination", page + 1)
        })

    for index, destination in enumerate(paginated_options):
        choices.append({"desc": (f"|g{destination}|n"),
                        "goto": ("menunode_confirm_travel", {"destination": destination})})

    return menu_text, choices

def handle_pagination(caller, raw_string):
    """
    Handle the player's input to change pages or select a destination
    """
    current_page = caller.db.get('current_page', 1)
    selected_destination = caller.db.get('selected_destination', None)
    identifiers = get_all_space_room_identifiers()
    total_pages = (len(identifiers) + OPTIONS_PER_PAGE - 1) // OPTIONS_PER_PAGE

    if raw_string.lower() == 'next':
        if current_page < total_pages:
            current_page += 1
            return menunode_set_destination(caller, raw_string, current_page = current_page, selected_destination = selected_destination)
        else:
            caller.msg("You are already on the last page.")

    elif raw_string.lower() == 'prev':
        if current_page > 1:
            current_page -= 1
            return menunode_set_destination(caller, raw_string, current_page = current_page, selected_destination = selected_destination)
        else:
            caller.msg("You are already on the last page.")
    elif raw_string.isdigit():
        choice = int(raw_string)
        if 0 <= choice < len(identifiers):
            destination = identifiers[choice]
            caller.msg(f"Destination set to {destination}")
            caller.db.selected_destination = destination
        else:
            caller.msg("Invalid choice. Please select a valid number.")
    else:
        caller.msg("Invalid input. Please type a number to select a destination or 'next' / 'prev' to navigate pages.")

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
        ship = self.search(player.db.active_ship)
        ship.db.key = new_name

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

