from evennia import create_object
from evennia import DefaultObject
from typeclasses.asteroids import Resource
from typeclasses.objects import ProjectSolObject, Object
import random
from data.resources import gases
from evennia import DefaultObject

class GasCloud(Object):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.resources = {}

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

    def generate_gas_contents(self):
        selected_resources = random.sample(list(gases.keys()), k = 3)
        tempdict = {}
        for item in selected_resources:
            tempdict[item] = gases[item]
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
    def generate_gascloud(cls):
        cloud = create_object(typeclass="typeclasses.gasclouds.GasCloud", key="Gas Cloud")
        cloud.generate_gas_contents()
        return cloud
    