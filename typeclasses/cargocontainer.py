import evennia
from typeclasses.objects import Object

class CargoContainer(Object):
    """
    Represents a cargo container capable of storing resources and objects.

    Attributes:
        capacity (int): The maximum storage capacity of the container in resource units or object spaces.
        stored (int): The current amount of storage space used by resources and objects.
        resources (dict): A dictionary containing the resources stored in the container. The keys are the resource names,
            and the values are the quantities.

    Methods:
        at_object_creation(): Called when the container is first created, sets up the initial capacity and storage attributes.
        add_resource(resource): Adds resources to the container's storage.
        add_object(object): Adds an object to the container's storage.
    """
    def at_object_creation(self):
        """
        Called when the container is first created. Sets up the initial capacity and storage attributes.
        """
        self.db.size = 100
        self.db.capacity = 1000
        self.db.stored = 0  
        self.db.resources = {}

    def add_resource(self, resource):
        """
        Adds resources to the container's storage.

        Args:
            resource (dict): A dictionary containing the resources to add to the container. The keys are the resource
                names, and the values are the quantities.

        Notes:
            - If the container reaches its capacity, the method will stop adding resources and send a message to the caller.
        """
        for item, quantity in resource.items():
            self.db.stored += quantity
            if self.db.stored > self.db.capacity:
                self.caller.msg("Container is full!")
                break  # Stop adding resources once the container is full
            else:
                if item not in self.db.resources:
                    self.db.resources[item] = quantity
                else:
                    self.db.resources[item] += quantity

    def add_object(self, object):
        """
        Adds an object to the container's storage.

        Args:
            object (Object): The object to add to the container.

        Notes:
            - If the container reaches its capacity, the method will send a message to the caller and prevent adding the object.
            - The object must have a 'size' attribute that represents the number of spaces it occupies in the container.
        """
        if self.db.stored < self.db.capacity:
            object.move_to(self)
            self.db.stored += object.size
        else:
            self.caller.msg("Container is full!")

    def check_manifest(self):
        self.caller.msg(self.db.resources)
