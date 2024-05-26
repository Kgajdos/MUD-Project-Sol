import evennia
from commands.weapons import WeaponCmdSet
import typeclasses
from typeclasses.objects import Object
from commands.command import Command
from evennia import default_cmds
from evennia import CmdSet
from evennia import InterruptCommand
from typeclasses.wearables import Wearable
import random

#### Start of weapon specific commands!
class CmdLoadWeapon(Command):
    """
    Loads the weapon currently in the player's hands. 
    
    Usage:
        reload
    """
    key = "reload"
    locks = "cmd:cmdarmed()"
    help_category = "Combat"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("What ammo?")
            raise InterruptCommand

    def func(self):
        item = self.caller.search("ammo", candidates = self.caller.contents)
        if not item: #if no item is found
            return
        if not item == "ammo":
            return self.caller.msg("You cannot load that into a gun.")

        _ammo = item.copy(new_key = item.key)
        #stores the ammo in the Gun
        _ammo.move_to(self.obj.contents)
        item.delete()
