from typing import Self
from evennia import Command, CmdSet, InterruptCommand
from pydantic import CallableError

class CmdShoot(Command):
    """ 
    Fires the held weapon

    Usage:
        shoot <target>
    """
    key = "shoot"
    locks = "cmd:cmdholds()"
    help_category = "Combat"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Shoot What?")
            raise InterruptCommand
    
    def func(self):
        target = self.caller.search(self.args.strip())
        if target:
            self.obj.attack(target)


class WeaponCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdShoot())