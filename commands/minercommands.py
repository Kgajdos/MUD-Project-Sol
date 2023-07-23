from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand
from evennia.utils import delay

class MineAsteroid(Command):
    """
    Command to initiate mining an asteroid.

    Usage:
        mine

    Notes:
        - The command must have a target asteroid specified before use.
        - The target asteroid is determined by the 'target' attribute in the object's database.
        - Initiates the mining process on the specified asteroid.
    """
    key = "mine"
    help_category = "Mining"

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

    Notes:
        - Stops the mining process on the targeted asteroid.
        - The targeted asteroid remains in the 'target' attribute in the object's database.
    """
    key = "stop mining"
    help_category = "Ship"

    def func(self):
        self.obj.stop_mining()

class MinerCmdSet(CmdSet):
    """
    Command set for a miner ship.

    Notes:
        - Contains commands related to mining asteroids and stopping the mining process.
    """
    key = "minercmdset"

    def at_cmdset_creation(self):
        self.add(MineAsteroid())
        self.add(StopMining())