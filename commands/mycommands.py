# in mygame/commands/mycommands.py
from evennia import DefaultCharacter, AttributeProperty, create_object
from typeclasses.characters import Character
from commands.command import Command
from evennia import default_cmds
from evennia import CmdSet
from evennia import InterruptCommand
from commands.wearables import CmdSetWear
from typeclasses.equipment import EquipmentHandler
from typeclasses.ships import Ships
from typeclasses import corporations
from evennia.contrib.game_systems import barter


class CmdCreateCorp(Command):
    """
    Create a corporation

    Usage:
        corporation <corp name>
    """
    key = "corporation"
    locks = "perm(builder)"
    help_category = "Building"
    

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.msg("Your corp needs a name.")
            raise InterruptCommand
    def func(self):
        corporations.create_corporation(self.args, self.caller)

class CmdLook(Command):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<account>

    Observes your location or objects in your vicinity.
    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
            if target == "Storage":
                ship = caller.location.location
                caller.msg(ship.return_ship_contents)
        else:
            target = caller.search(self.args)
            if not target:
                return
        desc = caller.at_look(target)
        # add the type=look to the outputfunc to make it
        # easy to separate this output in client.
        self.msg(text=(desc, {"type": "look"}), options=None)

class CmdWeild(Command):
    """
    Weild weapon

    Usage:
        wield <weapon_name>
    """
    key = "wield"
    locks = "cmd:wield()"
    
    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Test, something went wrong")
            raise InterruptCommand
        
    def func(self):
        weapon = self.caller.search(self.args, candidates = self.obj.contents)
        if not weapon:
            return
        weapon.do_wear(self.caller, weapon)

        

class CmdEcho(Command):
    """
    A simple echo command

    Usage:
        echo <something>

    """
    key = "echo"
    help_category = "General"

    def func(self):
        self.caller.msg(f"Echo: '{self.args.strip()}'")
        


class CmdHit(Command):
    """
    Hit a target.

    usage:
        hit <target>
    """
    key = "hit"
    help_category = "Combat"

    def parse(self):
        self.args = self.args.strip()
        target, *weapon = self.args.split(" with ", 1)
        if not weapon:
            target, *weapon = target.split(" ", 1)
        self.target = target.strip()
        if weapon:
            self.weapon = weapon[0].strip()
        else:
            self.weapon = ""

    def func(self):
        args = self.args.strip()
        if not args:
            self.caller.msg("Who do you want to hit?")
            return 
        # get the target for the hit
        target = self.caller.search(self.target)
        if not target:
            return
        # get and handle the weapon
        weapon = None
        if self.weapon:
            weapon = self.caller.search(self.weapon)
        if weapon:
            weaponstr = f"{weapon.key}"
        else:
            weaponstr = "bare fists"

        self.caller.msg(f"You hit {target.key} with {weaponstr}!")
        target.msg(f"You got hit by {self.caller.key} with {weaponstr}!")


class CmdShowWallet(Command):
    """
    Shows how many credits are in the player wallet.

    Usage:
        wallet
    """
    key = "wallet"
    locks = "cmd:all()"
    help_category = "Player"

    def func(self):
        caller = self.caller
        caller.msg(f"You have {caller.db.credit or 'no' } credits.")

class CmdPlayerSheet(Command):
    """
    Displays the player's character sheet.

    Usage:
        stats
    """
    key = "stats"
    locks = "cmd:all()"
    help_category = "Player"

    def func(self):
        caller = self.caller
        if not caller:
            return
        self.caller.msg(str(caller.player_sheet()))
        
class CmdEnterShip(Command):
    """
    Entering the ship.

    Usage:
        board ship
    """
    key = "board"
    locks = "cmd:not cmdinside();cmd: ispilot()"
    help_category = "Ship"

    def func(self):
        ship = self.obj.search(self.args)
        if not ship:
            return

        self.caller.msg("You board the ship.")
        self.caller.move_to(ship)

class CmdPutAway(Command):
    """
    Puts an item into the bag

    Usage:
        store <item_name> in <storage container>
    """
    key = "store"

    def parse(self):
        self.args = self.args.strip()
        item, *container = self.args.split(" in ", 1)
        self.item = item.strip()
        self.container = container[0].strip() if container else None

    def func(self):
        if not self.item:
            self.caller.msg("You must specify an item to store.")
            return

        item = self.caller.search(self.item)
        if not item:
            self.caller.msg(f"You do not have {self.item} in your hand.")
            return

        if self.container:
            container = self.caller.search(self.container)
            if not container:
                self.caller.msg(f"Storage container '{self.container}' not found.")
                return
            container.add(item)
            self.caller.msg(f"You store {item} in {container}.")
        else:
            self.caller.msg("You must specify a storage container.")



class CmdLeaveShip(Command):
    """
    Leaving the ship.

    Usage:
        disembark
    """
    key = "disembark"
    locks = "cmd:cmdinside()"
    help_category = "Ship"

    def func(self):
        self.caller.move_to(self.obj.location.location)



class ShipCmdSet(CmdSet):
    key = "shipcmdset"

    def at_cmdset_creation(self):
        self.add(CmdEnterShip())
        self.add(CmdLeaveShip())



class MyCmdGet(default_cmds.CmdGet):

    def func(self):
        super().func()
        self.caller.msg(str(self.caller.location.contents))

class MyCharCmdSet(CmdSet):
    
    def at_cmdset_creation(self):
        self.add(CmdEcho())
        self.add(CmdHit())
        self.add(CmdShowWallet())
        self.add(CmdPlayerSheet())
        self.add(CmdSetWear())
        self.add(ShipCmdSet())
        self.add(CmdWeild())
        self.add(CmdPutAway())
        self.add(CmdCreateCorp())
        self.add(barter.CmdsetTrade)