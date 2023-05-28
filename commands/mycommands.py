# in mygame/commands/mycommands.py
from evennia import DefaultCharacter, AttributeProperty, create_object
from typeclasses.characters import Character
from typeclasses.accounts import DefaultAccount
from commands.command import Command
from evennia import default_cmds
from evennia import CmdSet
from evennia import InterruptCommand
from commands.wearables import CmdSetWear
from typeclasses.ships import Ships


class CmdLogin(Command):
    """
    The login command

    Usage:
        login <character_name>

    """
    key = "login"
    alias = ["Login", "LOGIN", "l", "L"]
    help_category = "Account"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Login to who?")
            raise InterruptCommand

    def func(self):
        #Error with not finding whatever this returns
        #login = self.caller.search(self.args)
        login = Character.objects.filter(db_key=self.args)
        if not login:
            return
        try:
            self.caller.puppet_object(self.session, login)
        except AttributeError:
            self.caller.msg("You can't login to that.")

        

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
        board 
    """
    key = "board"
    locks = "cmd:not cmdinside()"
    help_category = "Ship"

    def func(self):
        ship = self.obj.db.ship
        if not ship:
            return

        self.caller.msg("You board the ship.")
        self.caller.move_to(ship)



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

class MyAccountCmdSet(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdLogin())