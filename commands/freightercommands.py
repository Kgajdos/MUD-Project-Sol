from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand

class CmdContracts(Command):
    key = "contract"
    help_category = "Freight"

    contract_switches = ("accept", "cancel", "check")

    def func(self):
        try:
            if self.contract_switches:
                return self.do_contract_switches()
        except:
            self.msg("Something went wrong, try again.")

    def do_contract_switches(self):

class CmdCheckManifest(Command):
    """
    Command to check the shipping manifest of the current cargo container.

    Usage:
        check manifest

    Notes:
        - Displays a list of resources and their quantities in the cargo container's shipping manifest.
        - The shipping manifest is a record of the resources stored in the cargo container.
        - It provides valuable information about the contents of the container.
    """
    key = "check manifest"
    help_category = "Freight"

    def func(self):
        self.check_manifest()

class CmdTradeCargo(Command):
    """
    Command to give cargo from the player's freighter to another object.

    Usage:
        trade <cargo> to <target>

    Example:
        trade crate-1 to Anderson

    Args:
        cargo (str): The name of the cargo resource to give from the freighter's cargo hold.
        target (str): The name of the target object (e.g., a space station) to give the cargo to.

    Notes:
        - This command is used to transfer cargo resources from the player's freighter to another object in the game world.
        - The cargo must be present in the freighter's cargo hold.
        - The target object must be in the same location as the freighter or accessible by some form of transport.
        - The player may need to take additional actions (e.g., docking, trading, etc.) to complete the transfer.

    """
    key = "trade"
    help_category = "Freight"

    def parse(self):
        self.args = self.args.split("to")
        if not self.args:
            self.msg("Trade what?")
            raise InterruptCommand
        if not self.args[1]:
            self.msg(f"Trade {self.args} to who?")
            raise InterruptCommand
        
    def func(self):
        self.obj.unload_container(self.args, self.args[1].contents)

class FreighterCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdCheckManifest())
        self.add(CmdTradeCargo())