from evennia import typeclasses
from typeclasses.characters import Character
from typeclasses.objects import Object
from evennia import Command, CmdSet, EvMenu
from evennia import InterruptCommand
import random


class NPCCmdSet(CmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdStoreShip())


class CmdStoreShip(Command):
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
        if ship:
            try:
                ship.move_to(self.obj)
                self.caller.msg(f"You have stored {ship.name}.")
            except:
                self.msg("Something went wrong.")
        else:
            self.caller.msg(f"You don't have a ship named {self.args}.")


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


class NPC(Character, Object):
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(NPCCmdSet())
        self.db.dialog_list = []

    def ship_service(self, shopper):
        menunodes = {
            "shipselect": node_shipselect,
            "end": node_end,
        }
        shopname = self.db.shopname or "The shop"
        EvMenu(
            shopper,
            menunodes,
            startnode="shipselect",
            shopname=shopname,
            shopkeeper=self,
            wares=self.contents,
        )

    def random_response(self):
        return random.choice(self.db.dialog_list)

    def add_dialog(self, dialog_line):
        self.db.dialog_list.append(dialog_line)

    def at_char_entered(self, character):
        """
        A simple is_aggressive check.
        Expand upon later - and make it more flexible.
        """
        if self.db.is_aggressive:
            self.execute_cmd(f"say Die {character}!")
        else:
            self.execute_cmd(f"say Greetings, {character}!")


def _handle_answer(caller, raw_input, **kwargs):
    answer = kwargs.get("answer")
    caller.msg(f"BEEP: Retrieving {answer}!")
    return "end"  # name of next node


def node_shipselect(caller, raw_input, **kwargs):
    "Top of the menu screen."
    menu = caller.ndb._evmenu
    shopname = menu.shopname
    shopkeeper = menu.shopkeeper
    ships = shopkeeper.contents
    text = f"Welcome to {shopname}!\n"

    options = []
    for ship in ships:
        options.append(
            {
                "key": f"{ship.key}",
                "desc": f"{ship.desc}",
                "goto": _handle_answer,
                "answer": ship,
            }
        )

    return text, options


def node_end(caller, raw_input, **kwargs):
    text = "Take care!"
    return text, None  # empty options ends the menu
