from evennia import Command, CmdSet, InterruptCommand


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
        ship = self.obj
        if not ship:
            return

        self.caller.msg("You board the ship.")
        self.caller.move_to(self.obj)



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
        self.caller.move_to(self.obj.location)



class ShipCmdSet(CmdSet):
    key = "shipcmdset"

    def at_cmdset_creation(self):
        self.add(CmdEnterShip())
        self.add(CmdLeaveShip())


