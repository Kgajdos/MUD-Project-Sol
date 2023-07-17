from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand
from evennia.utils import delay

class CmdLook(default_cmds.CmdLook):
    def func(self):
        # get regular look, followed by a combat summary
        super().func()

class Scan(Command):
    """
    Scan command for scanning the resource contents of a target object.

    Usage:
      scan <target>

    This command allows the player to scan the resource contents of a specific object.
    The command takes a single argument, which is the name or keyword of the target object
    to be scanned. The command will search for the target object in the current location of
    the player.

    Examples:
      scan asteroid
      scan cargo_ship

    Once the scan is initiated, a message will be displayed to the player indicating that
    the scanning process is taking place. After a short delay of 5 seconds, the results of
    the scan will be sent to the player, showing the resource contents of the target object.

    Note:
      - The scan command relies on the `scan` method of the target object, which should be
        implemented to handle the scanning functionality and provide the scan results.
      - The command assumes that the target object has the attribute `db.resource_contents`,
        which stores the resource contents of the object to be scanned.
    """
    key = "scan"
    help_category = "Ship"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Target what?")
            raise InterruptCommand

    def func(self):
        target = self.caller.search(self.args, candidates = self.caller.location.location)
        self.caller.msg("Scanning...")
        delay(5, self.obj.scan, self.caller, target)

class Target(Command):
    """
    Target command for selecting a target object.

    Usage:
      target <object>

    This command allows the player to select a target object for their ship's actions or systems.
    The command takes a single argument, which is the name or keyword of the object to be targeted.
    The command will search for the target object among the contents of the player's current location.

    Examples:
      target enemy_ship
      target asteroid

    Once the target is selected, it will be assigned to the `db.target` attribute of the invoking object.
    The `db.target` attribute can then be accessed by other systems or actions to perform actions or
    calculations related to the selected target.

    Note:
      - The `target` command relies on the `search` method of the invoking object, which should be
        implemented to handle object searching functionality.
      - The target object will be assigned to the `db.target` attribute of the invoking object.
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
        self.obj.target(target)

class UnloadCargo(Command):
    key = "unload"
    locks = "cmd:commandinstorage()"
    help_category = "Ship"

    def parse(self):
      self.args = self.args.strip()
      if not self.args:
          self.caller.msg("Unload what?")
          raise InterruptCommand
        
    def func(self):
        #TODO: Implement ship functions that check inventory
        pass

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
        self.add(StopPiloting())
        self.add(Scan())
        self.add(Target())
        self.add(CmdLook())
        