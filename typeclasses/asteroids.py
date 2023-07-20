from evennia import create_object
from evennia import DefaultObject
from typeclasses.objects import ProjectSolObject, Object
import random
from data.resources import minerals
from evennia import DefaultObject


class Resource(Object):
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

    def at_desc(self, looker=None, **kwargs):
        return super().at_desc(looker, **kwargs)

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


class Asteroid(Object):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resources = {}

    def at_object_creation(self):
        self.tags.add("Resource")

    def add_resource(self, resource, quantity):
        """
        Add a resource to the asteroid.

        Args:
            resource (Resource): The resource enum.
            rarity (str): The rarity level of the resource.

        Notes:
            This method stores the resource and its quantity in the asteroid's resource_contents dictionary.
        """
        if self.db.resource_contents is None:
            self.db.resource_contents = {}
        self.db.resource_contents[resource] = quantity



    def generate_asteroid_contents(self):
        """
        Generate the contents of the asteroid.
        """
        selected_resources = random.sample(list(minerals.keys()), k = 8)
        tempdict = {}
        for item in selected_resources:
            tempdict[item] = minerals[item]
        for resource, rarity in tempdict.items():
            #Add quantity based on rarity
            resource_name = resource
            if rarity == "common":
                quantity = random.randint(50, 100)
            elif rarity == "uncommon":
                quantity = random.randint(25, 55)
            elif rarity == "rare":
                quantity = random.randint(10, 20)
            self.add_resource(resource_name, quantity)


    @classmethod
    def generate_asteroid(cls):
        """
        Generate a new asteroid with random resource contents.

        Returns:
            Asteroid: The newly generated asteroid object.
        """
        asteroid = create_object(typeclass = "typeclasses.asteroids.Asteroid", key="Asteroid")
        asteroid.generate_asteroid_contents()
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
    


        

