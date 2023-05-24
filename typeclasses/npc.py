from evennia import typeclasses
from typeclasses.characters import Character
from typeclasses.objects import Object
from evennia import Command, CmdSet, EvMenu
from evennia import InterruptCommand
import random


class NPCCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdRetrieveShip())
        self.add(CmdStoreship())

########SHIP RETRIEVAL SERVICE SOMMANDS
class CmdStoreship(Command):
    """
    A command to store your ship with ship storage services.
    Usage:
        ship <shipname>
    """
    key = "ship"
    help_category = "Ship"
    
    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Store which ship?")
            raise InterruptCommand
        
    def func(self):
        ship = self.caller.search(self.args)
        try:
            ship.move_to(self.obj.contents)
        except:
            self.msg("Something went wrong.")

class CmdRetrieveShip(Command):
    """
    A command to open up the ship retrieval service.

    Usage:
        valet
    """
    key = "valet"
    help_category = "Menu"
    def func(self):
        self.obj.ship_service(self.caller)

class NPC(Object):

    def at_object_creation(self):
        self.cmdset.add_default(NPCCmdSet())

    def ship_service(self, shopper):
        menunodes = {
            "shipselect": node_shipselect,
            "end": node_end
        }
        shopname = self.db.shopname or "The shop"
        EvMenu(shopper, menunodes, startnode = "shipselect",
               shopname = shopname, shopkeeper = self, wares = self.contents)

    def random_response(self):
        return  random.choice(self.db.dialog_list)

    ##def load_quest(self):
    ## Import quest script and have it run from this command
    def add_dialog(self, dialog_line):
        self.db.dialog.append(dialog_line)

def _handle_answer(caller, raw_input, **kwargs):
    answer = kwargs.get("answer")
    caller.msg(f"BEEP: Retrieving {answer}!")
    return "end" #name of next node

#Needs to be fixed!
def node_shipselect(caller, raw_input, **kwargs):
    "Top of the menu screen."
    menu = caller.ndb._evmenu
    shopname = menu.shopname
    shopkeeper = menu.shopkeeper
    ships = shopkeeper.contents
    text = f"Welcome to {shopname}!"

    options = []
    for ship in ships:
        options.append = ({"key": f"{ship.key}",
               "desc": f"{ship.desc}",
               "goto": _handle_answer, "answer": ship})
    return text, options

def node_end(caller, raw_input, **kwargs):
    text = "Take care!"
    return text, None # empty options ends the menu


