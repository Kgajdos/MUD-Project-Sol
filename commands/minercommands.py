from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand
from evennia.utils import delay

class MineAsteroid(Command):
    key = "mine"
    help_category = "Ship"

    def parse(self):
        self.args = self.obj.db.target
        if not self.args:
            self.msg("You are not targeting anything.")
            raise InterruptCommand
        
    def func(self):
        self.obj.start_mining_asteroid(self.args)

class StopMining(Command):
    """
    Command to stop mining the asteroid.
    Does not delete target.

    Usage:
        stop mining
    """
    key = "stop mining"
    help_category = "Ship"

    def func(self):
        self.obj.stop_mining()

class MinerCmdSet(CmdSet):
    key = "minercmdset"

    def at_cmdset_creation(self):
        self.add(MineAsteroid())
        self.add(StopMining())