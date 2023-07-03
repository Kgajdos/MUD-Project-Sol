from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand
from evennia.utils import delay

class Scan(Command):
    """
    Command to return all objects in the room with the ship.
    Player is unable to utilize the look command while piloting!

    Usage:
        scan
    """
    key = "scan"
    help_category = "Ship"

    def func(self):
        self.caller.msg("Scanning...")
        delay(5, self.obj.scan, self.caller)

class Target(Command):
    """
    Command to target an in-game object saved to self.obj.scan_results

    Usage:
        target <object>
    """
    key = "target"
    help_category = "Ship"

    def parse(self):
        self.args = self.args.strip()

        if not self.args:
            self.caller.msg("Target what?")
            raise InterruptCommand
        
    def func(self):
        target = self.caller.search(self.args, candidates = self.caller.location.contents)
        self.obj.db.target = target



class MineAsteroid(Command):
    """
    Command to mine an asteroid. Must have a target
    """
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

class StopPiloting(Command):
    """
    Command to stop piloting the ship and become the PC again.

    Usage:
        stop flying
    """
    key = "stop flying"
    help_category = "Ship"

    def func(self):
        player = self.obj.db.pilot
        session = self.session 
        account = self.account
        account.puppet_object(session, player)

class ShipCmdSet(CmdSet):
    key = "shipcmdset"

    def at_cmdset_creation(self):
        self.add(MineAsteroid())
        self.add(StopPiloting())
        self.add(Scan())
        self.add(Target())