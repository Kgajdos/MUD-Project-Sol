import evennia
from evennia import DefaultObject, create_object
from commands.corpcommands import CorpoCmdSet

def create_corporation(name, leader):
    # create a new corporation, with the key as the name.
    new_corp = create_object(Corporation, key=name, location = None)
    new_corp.db.employees[leader] = "CEO"
    # set the leader as ceo and add cmdset to player.
    new_corp.db.leaders[leader] = "CEO"
    leader.db.corporation = new_corp
    leader.cmdset.add(CorpoCmdSet())

    # return the new corp.
    return new_corp

class Corporation(DefaultObject):
    """
    Represents a corporation in the game world.

    Attributes:
        reserves (dict): A dictionary containing the corporation's resource reserves. The keys are the resource names,
            and the values are the quantities.

    Methods:
        add_to_reserves(resource): Adds resources to the corporation's reserves.
        take_from_reserves(resource): Takes resources from the corporation's reserves.
        pay_employee(employee, credits): Pays an employee with credits.
        hire_employee(employee, player_class): Hires an employee and assigns them a player class.
        fire_employees(employee): Fires an employee and removes them from the corporation's employee list.
        show_employees(): Displays a list of employed players and their assigned player classes.
        promote(employee, title): Promotes an employee to a leadership position.
        demote(employee): Demotes an employee from a leadership position.
        create_cargo_crate(resources, object): Creates a cargo crate and adds resources or an object to it.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.leaders = {}
        self.db.employees = {}
        self.db.reserves = {}

    def add_to_reserves(self, resource):
        """
        Adds resources to the corporation's reserves.

        Args:
            resource (dict): A dictionary containing the resources to add to the reserves. The keys are the resource
                names, and the values are the quantities.

        Notes:
            - If a resource already exists in the reserves, its quantity is incremented.
            - If a resource does not exist in the reserves, it is added with the specified quantity.
        """
        for item, quantity in resource.items():
            if not item in self.db.reserves:
                self.db.reserves[item] = quantity
            else:
                self.db.reserves[item] += quantity

    def take_from_reserves(self, resource):
        """
        Takes resources from the corporation's reserves.

        Args:
            resource (dict): A dictionary containing the resources to take from the reserves. The keys are the resource
                names, and the values are the quantities.

        Notes:
            - If a resource exists in the reserves and the quantity requested is available, it is subtracted from the
                reserves.
            - If a resource does not exist in the reserves or the requested quantity is not available, no action is taken.
        """
        for item, quantity in resource.items():
            if self.db.reserves[item]:
                self.db.reserves[item] -= quantity

    def display_reserves(self):
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

        Notes:
            - The specified amount of credits is added to the employee's db.credits attribute.
            - If the employee is not a member of this corporation, an error message is sent to the caller.
        """
        if employee in self.db.employees.values():
            employee.db.credits += credits
        else:
            self.caller.msg(f"{employee} is not a member of this corporation")

    def hire_employee(self, employee, player_class):
        """
        Hires an employee and assigns them a player class.

        Args:
            employee (Object): The object representing the employee to be hired.
            player_class (str): The player class to be assigned to the employee.

        Notes:
            - If the employee is not already in the corporation's employee dictionary, they are added with the specified player class.
            - If the employee is already in the dictionary, their player class is updated to the new value.
        """
        if employee not in self.db.employees:
            self.db.employees[employee] = player_class

    def fire_employee(self, employee):
        """
        Fires an employee and removes them from the corporation's employee list.

        Args:
            employee (Object): The object representing the employee to be fired.

        Notes:
            - If the employee is in the corporation's employee dictionary, they are removed from the dictionary.
            - If the employee is not found in the dictionary, nothing happens.
        """
        if employee in self.db.employees:
            self.db.employees[employee].pop()

    def show_employees(self):
        """
        Displays a list of employed players and their assigned player classes.

        Notes:
            - Iterates through the corporation's employee dictionary and sends a message to the corporation object (self) for each entry.
            - Each message shows the employee and their assigned player class.
        """
        for item, player_class in self.db.employees.items():
            self.msg(f"{item} is employed and is a {player_class}.")

    def promote(self, employee, title):
        """
        Promotes an employee to a leadership position.

        Args:
            employee (Object): The object representing the employee to be promoted.
            title (str): The title or position to be assigned to the employee as a leader.

        Notes:
            - If the specified title does not already exist in the corporation's leaders dictionary,
              the employee is assigned to that title.
            - The employee is granted access to the Corporation Command Set (CorpoCmdSet).
        """
        if not self.db.leaders[title]:
            self.db.leaders[title] = employee

        employee.add(CorpoCmdSet())

    def demote(self, employee):
        """
        Demotes an employee from a leadership position.

        Args:
            employee (Object): The object representing the employee to be demoted.

        Notes:
            - If the employee is in the corporation's leaders dictionary, they are removed from the dictionary,
              effectively demoting them from the leadership position.
            - The employee loses access to the Corporation Command Set (CorpoCmdSet).
        """
        if employee in self.db.leaders:
            self.db.leaders[employee].pop()
            employee.remove(CorpoCmdSet())

    def create_cargo_crate(self, resources, object):
        """
        Creates a cargo crate and adds resources or an object to it.

        Args:
            resources (dict, optional): A dictionary containing the resources to add to the cargo crate.
                The keys are the resource names, and the values are the quantities.
            object (Object, optional): An object to add to the cargo crate.

        Notes:
            - If both resources and an object are provided, resources will be added first until the cargo crate is full.
            - If the cargo crate becomes full before all resources are added, the remaining resources are not added.
            - If the cargo crate becomes full before the object is added, the object will not be added.
        """
        crate = create_object(typeclass = "typeclasses.cargocontainer.CargoContainer", key = "Crate", location = self.location)
        if resources:
            crate.add_resource(resources)
        elif object:
            crate.add_object(object)
        return crate

    def load_ship(self, crate, ship):
        """
        Loads a cargo crate into a ship.

        Args:
            crate (Object): The cargo crate to be loaded into the ship.
            ship (Object): The ship into which the cargo crate will be loaded.

        Notes:
            - Moves the cargo crate to the contents of the ship, effectively loading it into the ship.
        """
        self.move_crate(crate, ship.contents)

    def move_crate(self, crate, location):
        """
        Moves a cargo crate to a specified location.

        Args:
            crate (Object): The cargo crate to be moved.
            location (Object): The location to which the cargo crate will be moved.

        Notes:
            - If the `crate` object is found in the caller's current location, it will be moved to the `location`.
            - If the `crate` object is not found in the caller's current location, an error message will be displayed.
        """
        try:
            if self.search(crate):
                crate.move_to(location)
        except:
            self.caller.msg(f"{crate} not found.")