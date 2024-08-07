from evennia import DefaultObject, create_object
from evennia.commands.cmdset import CmdSet
from evennia import EvMenu, search_object
from evennia.utils.evmenu import EvMenuError
from evennia import Command, ObjectDB
from typeclasses.objects import Object
from typeclasses.corporations import Corporation
from evennia.utils import logger

class CmdCorporateComputer(Command):
    """
    Opens the Corporate Computer

    Usage:
        computer
    """
    key = "computer"
    help_category = "Corporate"

    def func(self):
        if not self.obj:
            self.caller.msg("Error: No computer object found.")
            return
        try:
            self.obj.start_computer(self.caller, self.session)
        except Exception as e:
            self.caller.msg(f"An error occurred: {e}")

class CorpoCompCmdSet(CmdSet):
    key = "corpocompcmdset"

    def at_cmdset_creation(self):
        self.add(CmdCorporateComputer())

class CorpoComputer(Object):
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add(CorpoCompCmdSet())
        self.db.desc = "A sleek grey terminal with the Basic Space logo on it."

    def start_computer(self, player, session):
        """
        Start the Corporate Computer:

        Args:
            player (Player): The player using the computer.
            session (Session): The session through which the player is interacting.
        """
        menunodes = {
            "menunode_start": menunode_start,
            "menunode_sell": menunode_sell,
            "menunode_quantity": menunode_quantity,
            "_confirm_sale": _confirm_sale
        }

        try:
            EvMenu(player, menunodes, startnode="menunode_start", session=session)
        except EvMenuError as e:
            player.msg(f"Error initializing menu: {e}")
        except Exception as e:
            player.msg(f"An error occurred while starting the computer: {e}")

def menunode_start(caller):
    text = f"Welcome to the Basic Space Network, {caller.key}. Enter quit or q to exit."
    options = [{
        "desc": "Sell Cargo",
        "goto": "menunode_sell"
    }]
    return text, options


def menunode_sell(caller):
    from typeclasses.ships import Ships
    ship_key = caller.db.active_ship

    if not ship_key:
        caller.msg("Error: No active ship found.")
        return

    # Query using the correct field name
    all_ships = Ships.objects.filter_family(db_attributes__db_key="shipid", db_attributes__db_value=ship_key)
    
    if not all_ships:
        caller.msg("Ship not found.")
        return

    ship = all_ships.first()
    cargo = ship.db.cargo
    
    if not ship.attributes.has('cargo'):
        caller.msg("Error: Cargo data missing.")
        return

    else:
        text = "Select an item number to sell:"
        options = [{"desc": f"{item} ({quantity})", "goto": ("menunode_quantity", {"item_name": item})} for item, quantity in cargo.items()]
        options.append({"desc": "Go Back", "goto": "menunode_start"})
        #print(text, options)
        return text, options

def menunode_quantity(caller, raw_string, **kwargs):
    item_name = kwargs.get("item_name")
    text = f"Enter the quantity to confirm sale of {item_name}:"
    options = [
        {"key": "_default", "goto": ("_confirm_sale", {"item_name": item_name})},
        {"desc": "Go Back", "goto": "menunode_sell"}
    ]

    return text, options


def _confirm_sale(caller, raw_string, **kwargs):
    item_name = kwargs.get("item_name")
    quantity = raw_string.strip()
    
    if not quantity.isdigit():
        caller.msg("Error: Invalid quantity. Please enter a number.")
        return "menunode_quantity", {"item_name": item_name}
    
    quantity = int(quantity)
    ship_key = caller.db.active_ship
    
    if not ship_key:
        caller.msg("Error: No active ship found.")
        return
    
    # Query using the correct field name
    from typeclasses.ships import Ships
    all_ships = Ships.objects.filter_family(db_attributes__db_key="shipid", db_attributes__db_value=ship_key)
    
    if not all_ships:
        caller.msg("Ship not found.")
        return
    
    ship = all_ships.first()

    cargo = ship.db.cargo
    if not cargo:
        caller.msg("Error: Cargo data missing.")
        return
    
    logger.info(f"{item_name}")

    if item_name not in cargo:
        caller.msg(f"Error: No cargo item named '{item_name}' found.")
        return "menunode_sell"
    
    if quantity > cargo[item_name]:
        caller.msg(f"Error: You don't have that much {item_name} to sell.")
        return "menunode_quantity", {"item_name": item_name}
    
    # Update cargo quantity
    cargo[item_name] -= quantity
    if cargo[item_name] <= 0:
        del cargo[item_name]
    ship.db.cargo = cargo
    
    caller.msg(f"Sold {quantity} of {item_name}.")
    options = [
        {"desc": "Return to sell menu"},
        {"goto": menunode_sell}
    ]
    return options