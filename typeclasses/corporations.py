import evennia
from evennia import DefaultObject, create_object
from commands.corpcommands import CorpoCmdSet
##from contract import ContractHandler

def create_corporation(name, leader):
    new_corp = create_object(Corporation, key=name, location=None)
    new_corp.db.employees = {leader: "CEO"}
    new_corp.db.leaders = {leader: "CEO"}
    leader.db.corporation = new_corp
    leader.cmdset.add(CorpoCmdSet())

    return new_corp

class Corporation(DefaultObject):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.leaders = {}
        self.db.employees = {}
        self.db.reserves = {}
        self.db.jobs = []
        self.db.contracts = []

    def add_to_reserves(self, resource):
        """
        Adds resources to the corporation's reserves.

        Args:
            resource (dict): A dictionary containing the resources to add to the reserves. The keys are the resource
                names, and the values are the quantities.
        """
        for item, quantity in resource.items():
            if item not in self.db.reserves:
                self.db.reserves[item] = quantity
            else:
                self.db.reserves[item] += quantity

    def take_from_reserves(self, resource):
        """
        Takes resources from the corporation's reserves.

        Args:
            resource (dict): A dictionary containing the resources to take from the reserves. The keys are the resource
                names, and the values are the quantities.
        """
        for item, quantity in resource.items():
            if item in self.db.reserves and self.db.reserves[item] >= quantity:
                self.db.reserves[item] -= quantity

    def display_reserves(self):
        """
        Displays the current resource reserves of the corporation.
        """
        temp_dict = {}
        for item, quantity in self.db.reserves.items():
            if item not in temp_dict:
                temp_dict[item] = quantity
            else:
                temp_dict[item] += quantity
        self.msg(f"Corporate Reserves: {temp_dict}.")

    def pay_employee(self, employee, credits):
        """
        Pays an employee with credits.

        Args:
            employee (Object): The employee to be paid.
            credits (int): The amount of credits to pay the employee.
        """
        if employee in self.db.employees:
            employee.db.credits += credits
        else:
            self.caller.msg(f"{employee} is not a member of this corporation")

    def hire_employee(self, employee, player_class):
        """
        Hires an employee and assigns them a player class.

        Args:
            employee (Object): The object representing the employee to be hired.
            player_class (str): The player class to be assigned to the employee.
        """
        self.db.employees[employee] = player_class

    def fire_employee(self, employee):
        """
        Fires an employee and removes them from the corporation's employee list.

        Args:
            employee (Object): The object representing the employee to be fired.
        """
        if employee in self.db.employees:
            del self.db.employees[employee]

    def show_employees(self):
        """
        Displays a list of employed players and their assigned player classes.
        """
        for employee, player_class in self.db.employees.items():
            self.msg(f"{employee} is employed as a {player_class}.")

    def promote(self, employee, title):
        """
        Promotes an employee to a leadership position.

        Args:
            employee (Object): The object representing the employee to be promoted.
            title (str): The title or position to be assigned to the employee as a leader.
        """
        self.db.leaders[title] = employee
        employee.cmdset.add(CorpoCmdSet())

    def demote(self, employee):
        """
        Demotes an employee from a leadership position.

        Args:
            employee (Object): The object representing the employee to be demoted.
        """
        for title, leader in self.db.leaders.items():
            if leader == employee:
                del self.db.leaders[title]
                break
        employee.cmdset.remove(CorpoCmdSet())

    def create_cargo_crate(self, resources=None, object=None):
        """
        Creates a cargo crate and adds resources or an object to it.

        Args:
            resources (dict, optional): A dictionary containing the resources to add to the cargo crate.
                The keys are the resource names, and the values are the quantities.
            object (Object, optional): An object to add to the cargo crate.

        Returns:
            Object: The created cargo crate object.
        """
        crate = create_object("typeclasses.cargocontainer.CargoContainer", key="Crate", location=self.location)
        if resources:
            crate.db.resources = resources
        elif object:
            crate.db.object = object
        return crate

    def load_ship(self, crate, ship):
        """
        Loads a cargo crate into a ship.

        Args:
            crate (Object): The cargo crate to be loaded into the ship.
            ship (Object): The ship into which the cargo crate will be loaded.
        """
        self.move_crate(crate, ship)

    def move_crate(self, crate, location):
        """
        Moves a cargo crate to a specified location.

        Args:
            crate (Object): The cargo crate to be moved.
            location (Object): The location to which the cargo crate will be moved.
        """
        if crate.location == self.location:
            crate.move_to(location)
        else:
            self.msg(f"{crate} not found in the current location.")

    def post_job(self, description, reward, task_details):
        job = ContractHandler.create_job(description, reward, task_details)
        self.db.jobs.append(job)
        self.msg(f"Job posted: {description} for {reward} credits.")

    def post_contract(self, sender, receiver, cargo, weight, destination, reward, expiry_date=None):
        contract = ContractHandler.create_freight_contract(sender, receiver, cargo, weight, destination, reward, expiry_date)
        self.db.contracts.append(contract)
        self.msg(f"Contract posted: {contract.description} for {contract.reward} credits.")

    def show_jobs(self):
        if not self.db.jobs:
            self.msg("No jobs available.")
        for job in self.db.jobs:
            self.msg(f"Job: {job.description}, Reward: {job.reward} credits, Task: {job.task_details}.")

    def show_contracts(self):
        if not self.db.contracts:
            self.msg("No contracts available.")
        for contract in self.db.contracts:
            self.msg(f"Contract: {contract.description}, Reward: {contract.reward} credits, Cargo: {contract.cargo}.")

    def complete_job(self, job, player):
        """
        Completes a job and pays the player.

        Args:
            job (Job): The job to be completed.
            player (Object): The player who completed the job.
        """
        if job.complete(player):
            self.db.jobs.remove(job)
            self.msg(f"Job completed: {job.description}. {player.name} has been paid {job.reward} credits.")
        else:
            self.msg("Job could not be completed.")

    def complete_contract(self, contract, player):
        """
        Completes a contract and pays the player.

        Args:
            contract (FreightContract): The contract to be completed.
            player (Object): The player who completed the contract.
        """
        if contract.complete(player):
            self.db.contracts.remove(contract)
            self.msg(f"Contract completed: {contract.description}. {player.name} has been paid {contract.reward} credits.")
        else:
            self.msg("Contract could not be completed.")

