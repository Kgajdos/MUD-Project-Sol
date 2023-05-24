from typeclasses.objects import Object
from evennia.objects.objects import DefaultRoom
from evennia import Command, CmdSet
from evennia import InterruptCommand

class CmdOpenBag(Command):
    """
    Displays the contents in bag

    Usage:
        bag
    """
    key = "bag"
    def parse(self):
        self.args = self.args.strip()
    
    def func(self):
        #self.obj is bag, self.caller is pc
        self.caller.msg(self.obj.contents)

class CmdPutAway(Command):
    """
    Puts an item into the bag

    Usage:
        store <item_name> in <storage container>
    """
    key = "store"

    def parse(self):
        self.args = self.args.strip()
        item, *container = self.args.split(" in ", 1)
        self.item = item.strip()
        if container: #sets the container if there is one specified
            self.container = container[0].strip()
        else:
            self.container = "" #defaults to no container

    def func(self):
        items = self.caller.search(self.item)
        if items:
            item = items[0]
        else:
            self.caller.msg(f"You do not have {items} in your hand.")
            return

        item = self.caller.search(items)
        container = self.obj.search(self.container)
        if not container:
            self.caller.msg(f"You do not see {container.key}")

        container.store_item(self.caller, item)

class CmdRetrieve(Command):
    """
    Retrieves an item from the bag

    Usage:
        retrieve <item_name> from <storage container>
    """
    key = "retrieve"

    def parse(self):
        self.args = self.args.strip()
        item, *container = self.args.split(" from ", 1)
        self.item = item.strip()
        if container:
            self.container = container[0].strip()
        else:
            self.container = ""

    def func(self):
        item_name = self.item
        if not item_name:
            self.caller.msg("Retrieve what?")
            raise InterruptCommand
        item = self.caller.search(item_name)
        container = self.obj.search(self.container)
        if not container:
            self.caller.msg(f"You do not see {container.key}")
        container.retrieve_item(self.caller, item_name)
        self.caller.msg(f"You grab {item_name}.")


class BagCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdOpenBag())
        self.add(CmdPutAway())
        self.add(CmdRetrieve())
    
class Bag(Object):
    
    def at_object_creation(self):
        self.db.desc = "A sturdy canvas bag to hold all your belongings."


    def store_item(self, caller, item_name):
        item_name.move_to(self, quiet=True, move_type = "store")
        caller.msg(f"You store {item_name} in your bag.")

    def retrieve_item(self, caller, item_name):
        if not self.search(item_name):
            caller.location.msg(f"There is no {item_name} in your bag.")

        item = self.search(item_name)
        item.move_to(caller, quiet=True, move_type="retrieve")
        caller.location.msg(f"You grab {item.key} from your bag.")


class Chest(Bag):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.desc = "A sturdy wooden chest."

    def store_item(self, caller, item_name):
        super().store_item(caller, item_name)
        caller.msg(f"You store {item_name} in {self.key}")

    def retrieve_item(self, caller, item_name):
        super().retrieve_item()
        caller.location.msg(f"You grab {item.key} from {chest.key}")

    