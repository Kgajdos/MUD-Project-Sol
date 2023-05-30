import datetime
from typeclasses import ships
from typeclasses.objects import Object
from evennia import InterruptCommand
from evennia import Command, CmdSet, create_object, search_object, EvMenu, EvForm, EvTable

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
        {"desc": f"|cRename Ship|n", "goto": "menunode_ship_rename"
    }]
    return text, options

def menunode_help(caller, raw_string, **kwargs):
    text = f"""Welcome to your ship! You are accessing your onboard computer system. Here you can check out your ships statistics sheet, as well as cargo currently in storage.
Every ship comes with a Captain's log for your convienence.

To make things simpler, your options are color coded:
|cCyan|n: This means you are about to interact with or modify your ship. (example: new Captain's log.)
|gGreen|n: This means you are revieving information about your ship.
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

def menunode_ship_rename(caller, raw_string, **kwargs):
    text = f"""Type in a new name for your ship and press enter. 
|rWARNING: You will not be notified of this change!|n"""

    options = {"key": "_default", "goto": _new_name}

    return text, options

def _new_name(caller, raw_string, **kwargs):
    menu = caller.ndb._evmenu
    menu.ai.set_new_name(caller, raw_string)

    return "menunode_start"

class ShipConsole(Object):

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(ConsoleCmdSet())
        self.db.desc = "This is the main computer of the ship. Here is where you can access things like your Captain's log, or take a look at your ship stats."
        self.db.logs = []

    def start_consoles(self, player):
        menunodes = {
            "menunode_start": menunode_start,
            "_ship_stats": _ship_stats,
            "menunode_help": menunode_help,
            "menunode_captains_logs": menunode_captains_logs,
            "menunode_new_log": menunode_new_log,
            "menunode_choose_log": menunode_choose_log,
            "menunode_read_log": menonode_read_log,
            "menunode_ship_rename": menunode_ship_rename
        }
        consolename = self.db.name or "Admin"
        EvMenu(player, menunodes, startnode = "menunode_start",
               consolename = consolename, ai = self, console = self.contents)
        
    def set_new_name(self, player, new_name):
        player.db.active_ship = new_name
        ship = self.location.location
        ship.key = new_name
        ship.name = new_name

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

        return str(form)

    def store_cargo(self, cargo, player):
        cargo.move_to(self)
        player.msg(f"You store {cargo.key} in your ship.")
        #_SHIP_CONSOLE_DICT.append({cargo})#This exists as a potenial solution to allow items to be stored in the console but displayed in the Storage room!
        #The idea is by creating a dict with the cargo key, it can be easily accessed by other parts of the ship