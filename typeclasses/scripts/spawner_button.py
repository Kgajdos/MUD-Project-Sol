import evennia
from evennia import create_object, DefaultScript



class ButtonSpawn(DefaultScript):
    def at_script_creation(self):
        self.key = "spawnbutton"
        