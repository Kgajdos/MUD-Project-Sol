from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand

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
        pass #TODO: Implement mining function in ship class