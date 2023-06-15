from evennia import create_object
from evennia import DefaultObject
from typeclasses.objects import ProjectSolObject, Object
import random

from evennia import DefaultObject
from typeclasses.asteroids import ProjectSolObject


class Resource(ProjectSolObject):
    """
    Represents a resource object.

    Attributes:
        quantity (int): The quantity of the resource.

    Properties:
        quantity (int): Get or set the quantity of the resource.

    Methods:
        add_quantity(amount): Add to the quantity of the resource.
        remove_quantity(amount): Remove from the quantity of the resource.
        display(): Return a string representation of the resource.
    """
    def at_object_creation(self):
        """
        Called when the resource is first created.
        """
        self.db.quantity = 0

    @property
    def quantity(self):
        """
        Get the quantity of the resource.
        """
        return self.db.quantity

    @quantity.setter
    def quantity(self, value):
        """
        Set the quantity of the resource.
        """
        self.db.quantity = value

    def add_quantity(self, amount):
        """
        Add to the quantity of the resource.
        """
        self.db.quantity += amount

    def remove_quantity(self, amount):
        """
        Remove from the quantity of the resource.
        """
        self.db.quantity -= amount

    def display(self):
        """
        Return a string representation of the resource.
        """
        return f"{self.key}: {self.db.quantity}"


class Asteroid(ProjectSolObject, Object):
    """
    This is the Asteroid class. Asteroids are objects in space that provide the player with different resources.

    Attributes:
        resource_rarities (dict): A dictionary mapping resource names to their rarity levels.

    Methods:
        add_resource(resource, rarity): Add a resource to the asteroid.
        get_random_resource(): Get a random resource from the asteroid.
        generate_asteroid_contents(resource_ranges): Generate the contents of the asteroid.
        generate_asteroid(resource_quantities): Generate an asteroid with the specified resource quantities.
        display_resource_contents(): Return the resource contents of the asteroid as a string.
        mine_asteroid(mining_skill): Mine the asteroid and retrieve resources based on the mining skill.
    """

    resource_rarities = {
        "Iron": "common",
        "Nickle": "common",
        "Clay": "common",
        "Silver": "uncommon",
        "Gold": "rare",
        "Platinum": "rare",
        "Silicate": "rare"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = {}

    def at_object_creation(self):
        self.tags.add("Resource")

    def add_resource(self, resource, rarity):
        if rarity not in self.resources:
            self.resources[rarity] = []
        self.resources[rarity].append(resource)

    def get_random_resource(self):
        all_resources = []

        for rarity in self.resources:
            all_resources.extend(self.resources[rarity])

        if not all_resources:
            return None
        
        return random.choice(all_resources)
    
    def generate_asteroid_contents(self, resource_ranges):
        """
        Generate the contents of the asteroid.
        """
        contents = {}
        for resource_name, quantity_range in resource_ranges.items():
            resource_quantity = random.randint(quantity_range[0], quantity_range[1])
            contents[resource_name] = resource_quantity
        self.db.resource_contents = contents
    
    @classmethod
    def generate_asteroid(self, resource_quantities):
        """
        Generate the asteroid with the specified resource quantities.

        Args:
            resource_quantities (dict): A dictionary of resource quantities, where the keys are the resource names
                                    and the values are the quantities.

        Returns:
            Asteroid(resource_quantities)
        """
        asteroid = create_object("typeclasses.asteroids.Asteroid", key="Asteroid")
        asteroid.db.resource_contents = resource_quantities
        return asteroid
    
    def display_resource_contents(self):
        """
        Return the resource contents of the asteroid as a string.
        """
        resource_contents = self.db.resource_contents
        if not resource_contents:
            return "No resources in the asteroid."

        resource_string = "\n".join([f"{name}: {quantity}" for name, quantity in resource_contents.items()])
        return resource_string
    
    def mine_asteroid(self, mining_skill):
        """
        Mine the asteroid and retrieve resources based on the mining skill.
        """
        resource_contents = self.db.resource_contents or {}
        mined_resources = {}
        for resource_name, quantity in resource_contents.items():
            mined_quantity = quantity * mining_skill  # Adjust quantity based on mining skill
            mined_resources[resource_name] = mined_quantity

        # Remove the mined resources from the asteroid
        for resource_name in mined_resources:
            del resource_contents[resource_name]

        self.db.resource_contents = resource_contents  # Update the remaining resource contents in the database

        return mined_resources


        

