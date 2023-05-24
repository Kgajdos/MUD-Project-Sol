import evennia
from commands.weapons import WeaponCmdSet
import typeclasses
from typeclasses.objects import Object
from commands.command import Command
from evennia import default_cmds
from evennia import CmdSet
from evennia import InterruptCommand
import random

#### Start of weapon specific commands!
class CmdLoadWeapon(Command):
    """
    Loads the weapon currently in the player's hands. 
    
    Usage:
        load_weapon
    """
    #Fix this eventually, this is not what I want
    key = "load_weapon"
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


class WeaponCmdSet(CmdSet):
    key = "weaponcmdset"
    def at_object_creation(self):
        self.add(CmdLoadWeapon())

#Parent class for all weapons
class Weapon(Object):
    
    def at_object_creation(self):
        self.cmdset.add_default(WeaponCmdSet())
        self.db.physical = random.randint(1, 10)

    def attack(self, target):
        #TODO: This is where a check against the targets physical would need to take place
        if target.db.physical < self.db.damage:
            damage = random.randint(1, 10) + 1
        else:
            damage = 1

        return damage
    
class Gun(Weapon):

    def at_object_creation(self):
        super().at_object_creation()


