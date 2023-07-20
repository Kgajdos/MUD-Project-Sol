import evennia
from evennia import DefaultObject

class Corporation(DefaultObject):

    def at_object_creation(self):
        self.db.reserves = {}