from evennia import Command, CmdSet, EvMenu
from typeclasses.objects import Object

class CmdCorporateComputer(Command):
    """
    Opens the Corporate Computer

    Usage:
        computer
    """
    key = "computer"
    help_category = "Corporate"

    def func(self):
        self.obj.start_computer(self.caller, self.session)

class CorpoComputer(Object):

    def at_object_creation(self):
        """
            Called when the object is created. Adds default console commands and initializes object properties.

            Notes:
                - This method is automatically called by Evennia during object creation.

        """
        super().at_object_creation()
        self.cmdset.add_default(CorpoCompCmdSet())
        self.db.desc = "A sleek grey terminal with the Basic Space logo on it. This computer connects to the Corporate network."

    def start_computer(self, player, session):
        """
        Start the Corporate Computer:

        Args:
            player (Player): The player using the computer.
            session (Session): The session through with the player is interacting.
        """
        menunodes = {
            "menunode_start": menunode_start,
            "menunode_sell": menunode_sell,
            "_confirm_sale": _confirm_sale
        }

class CorpoCompCmdSet(CmdSet):
    key = "corpoconsolecmdset"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdCorporateComputer())


###########################################################################################################
def menunode_start(caller):
    menu = caller.ndb._evmenu
    text = f"Welcome to the Basic Space Network {caller.key}. Enter quit or q to exit."
    options = [{
        "desc": f"|cSell Cargo|c", "goto": "menunode_sell"
    }]
    return text, options

def menunode_sell(caller):
    ship = caller.db.ship
    cargo = ship.db.cargo
    for item, value in cargo:
        caller.msg(f"{item}: Sells for {value} credits.")
    ##Figure out how to allow the player to input an item name
    options = [{
        "desc": f"|cSell <Item Name>|c", "goto": "_confirm_sale"
    }]

def _confirm_sale(caller, **kwargs):
    pass