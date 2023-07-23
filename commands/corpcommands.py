from commands.command import Command
from evennia import default_cmds, CmdSet, InterruptCommand
from typeclasses.freightcontracts import FreightContract

class CmdPayEmployee(Command):
    """
    Pay an employee from the corporation's funds.

    Usage:
        pay <employee> <amount>

    Arguments:
        <employee>: The name of the employee to pay.
        <amount>: The amount of credits to pay to the employee.

    Notes:
        - The command allows you to transfer credits from the corporation's funds to an employee.
        - Make sure to provide the correct amount in credits.
    """
    key = "pay"
    help_category = "Corporation"
    def parse(self):
        self.args = self.args.split()
        if not self.args:
            self.msg("Give how much to who?")
            raise InterruptCommand
        if not isinstance(int, self.args[1]):
            self.msg("Pay how much?")
            raise InterruptCommand
        if self.args[1] < 0:
            self.msg("You cannot take money away from the player!")
            raise InterruptCommand
        
    def func(self):
        self.pay_employee(self.args[0], self.args[1])

class CmdLoadFreight(Command):
    """
    Load freight into a ship's cargo hold.

    Usage:
        freight <crate> in <ship>

    Arguments:
        crate (str): The name or key of the cargo crate to be loaded.
        ship (str): The name or key of the ship into which the cargo crate will be loaded.

    Notes:
        - This command is used to load a cargo crate into a ship's cargo hold.
        - The cargo crate must be located in the same room as the character using the command.
        - The ship must also be in the same room as the character using the command.
    """
    key = "freight"
    help_category = "Freight"

    def parse(self):
        """
        Parse the input for the freight loading command.

        Notes:
            - Splits the input into crate and ship arguments using the "in" keyword.
            - Raises an InterruptCommand exception if either crate or ship argument is missing.
        """
        self.args = self.args.split("in")
        if not self.args:
            self.msg("Which crate is being loaded?")
            raise InterruptCommand
        if not self.args[1]:
            self.msg("Load crate into which ship?")
            raise InterruptCommand
      
    def func(self):
        """
        Execute the freight loading command.

        Notes:
            - Calls the load_ship method to load the specified crate into the specified ship.
        """
        self.load_ship(self.args[0], self.args[1])

class CmdFreightContract(Command):
    """
    Command for creating and managing freight contracts.

    Usage:
        contract [sender <name>] [receiver <name>] [cargo <resource_dict>] [reward <amount>] [expiration <time>]
        contract create

    Switches:
        - sender: Specifies the sender (player) of the freight contract.
        - receiver: Specifies the receiver (player or corporation) of the freight contract. Use "receiver" without an argument to remove the current receiver.
        - cargo: Specifies the resources to be transported in the contract as a dictionary.
        - reward: Specifies the amount of reward offered for completing the contract.
        - expiration: Specifies the expiration time for the contract.

    Examples:
        contract sender JohnDoe receiver MyCorporation cargo {'iron': 500, 'gold': 200} reward 1000 expiration 2d
        contract receiver

    Notes:
        - The `contract` command allows players to draft, modify, and create freight contracts.
        - Players can draft a contract step-by-step by using the switches.
        - The `create` switch is used to finalize and create the drafted contract.
        - If the "receiver" switch is provided without an argument, it removes the current receiver from the contract draft.
    """

    key = "contract"
    help_category = "Corporation"

    contract_switches = ("sender", "receiver", "cargo", "reward", "expiration", "create")

    @property
    def contract_draft(self):
        if self.caller.ndb.contract_draft is None:
            self.caller.ndb.contract_draft = FreightContract()
        return self.caller.ndb.contract_draft

    def func(self):
        try:
            if self.contract_switches:
                return self.do_contract_switches()
        except:
            self.msg("Something went wrong, try again.")

    def do_contract_switches(self):
        if "sender" in self.switches:
            sender = self.args
            self.contract_draft.sender = sender
        if "receiver" in self.switches:
            if not self.args:
                self.contract_draft.receiver = None
            else:
                receiver = self.args
                self.contract_draft.receiver = receiver
        if "cargo" in self.switches:
            cargo = self.args
            self.contract_draft.cargo = cargo
        if "reward" in self.switches:
            reward = self.args
            self.contract_draft.reward = reward
        if "expiration" in self.switches:
            expiration = self.args
            self.contract_draft.expiration = expiration
        if "create" in self.switches:
            sender = self.contract_draft.sender
            receiver = self.contract_draft.receiver
            cargo = self.contract_draft.cargo
            reward = self.contract_draft.reward
            expiration = self.contract_draft.expiration
            contract = FreightContract.create_contract(sender = sender,
                                                       receiver=receiver,
                                                       cargo=cargo,
                                                       reward=reward,
                                                       expiration=expiration)
            for item in cargo.items():
                if self.search(item):
                    contract.move_crate(item, self.contents)
            self.msg(f"Contract created.")
            return

        

class CorpoCmdSet(CmdSet):
    """
    Command set for corporation-related commands.

    Notes:
        - This command set is assigned to a character or object representing a corporation.
        - It includes various corporation-related commands such as paying employees and loading freight.
    """
    key = "corpocmdset"

    def at_cmdset_creation(self):
        """
        Called when the command set is created. Adds commands to the command set.

        Notes:
            - Adds CmdPayEmployee and CmdLoadFreight to the command set.
        """
        self.add(CmdPayEmployee())
        self.add(CmdLoadFreight())