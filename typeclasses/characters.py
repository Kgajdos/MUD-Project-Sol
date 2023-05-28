"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import evennia
from evennia.utils import utils
from evennia import DefaultCharacter, AttributeProperty
from typeclasses.bags import Bag, BagCmdSet
from evennia import scripts
from evennia.utils import create
from evennia import EvForm, EvTable
import random
import world.rules
from typeclasses.objects import ObjectParent




class Character(DefaultCharacter):
    """
    (class docstring)
    """

    def at_object_creation(self):     
        self.db.stats = {}
        self.db.worn = {
            "head": None, "body": None, "arms": None, "feet": None}
        self.db.weapon = None
        self.update_character_on_first_login()
        self.db.HP = self.db.stats["Health"]
        
        if self.db.contents:
            pc_bag = evennia.create_object("typeclasses.bags.Bag", key="Bag", location = self, attributes = [("desc", "A sturdy canvas bag to hold your belongings.")])
        
        
    #Belo is functions that set a new ship to the player based on their class
    def set_ship_by_pc_class(self):
        ship = evennia.create_object(f"typeclasses.ships.{self.db.player_class}", key = "Ship", location = self.location, attributes = [("class", f"{self.db.player_class}")])
        self.db.ship = ship

    #only to be called at first login!!!! otherwise we'll be drowning in more ships
    def update_character_on_first_login(self):
        self.set_char_description()
        self.set_ship_by_pc_class()
        self.set_stat("Mental")
        self.set_stat("Physical")
        self.set_stat("Social")
        self.db.stats["Health"] = random.randint(1,10) * self.db.stats.get("Physical")
        self.db.stats["Stamina"] = random.randint(1, 10) * (self.db.stats.get("Physical") + self.db.stats.get("Mental"))



    def get_display_desc(self, looker, **kwargs):
        return super().get_display_desc(looker, **kwargs)
################################################################
################################################################
###########REWORK THIS ITS NOT RIGHT!!##########################
    #sets the char description
    def set_char_description(self):
        sex = self.db.sex
        adj = "is"
        if sex == "male":
            pronoun = "he"
        elif sex == "female":
            pronoun = "she"
        else:
            pronoun = "they"
            adj = "are"
        self.db.desc = f"Before you stands {self.key}, {pronoun} {adj} {self.db.adjective} and {self.db.body_type}. \nThey have a {self.db.disposition} disposition."

    #To be called when a character learns a new skill for the first time
    def create_skill_set(self, raw_string):
        skill = self.raw_string


    def set_stat(self, stat):
        #get a random num between 1-10
        value = random.randint(1, 10)
        #check if stat is already in db
        if stat in self.db.stats:
            #add the Value
            self.db.stats[stat] += value
        else:
            self.db.stats[stat] = value

    def delete(self):
        bag = self.search("Bag", candidates=self.contents, typeclass = "typeclasses.bags.Bag")
        if bag:
            bag.delete()
        super().delete()

    def at_pre_move(self, destination, **kwargs):
        """
        Called byself.move_to when trying to move somewhere. If this returns false, the move is immediately cancelled.
        """
        if self.db.is_sitting:
            self.msg("You need to stand up first.")
            return False
        return True
    
    def add_credits(self, credits):
        self.db.credit = (self.db.credit or 0) + credits

    def train_skill(self, skill_trained, amount):
        value = self.attributes.get(skill_trained) * amount
        self.attributes.add(skill_trained, value)
        self.msg(f"You trained for {value}!")

    #NEEDS THOUROUGH TESTING!!!!
    def player_sheet(self):
        '''
        Takes advantage of the EvForm to create the character sheet.
        '''
        form = EvForm("typeclasses.playerform")
        form.map(cells={1: self.account.key,
                        2: self.key,
                        3: self.db.desc,
                        4: self.db.stats.get("Mental"),
                        5: self.db.stats.get("Physical"),
                        6: self.db.stats.get("Social"),
                        7: self.db.sex})
        # create the EvTables

        health = self.db.stats["Health"]
        stamina = self.db.stats["Stamina"]
        tableA = EvTable("HEALTH", "STAMINA",
                         table=[[health], [stamina]],
                         border="incols")
        tableB = EvTable("Skill", "Value", "Exp")
        for skill_name, data in self.db.skills.items():
            tableB.add_row(skill_name, data.get("level", 0),
                           data.get("xp", 0),
                           border="incols")
        #map 'literal' replacents 
        custom_mapping = {"v&": "v2"}

        form.map(tables={"A": tableA,
                         "B": tableB},
                         literals=custom_mapping)
        return form
        
        
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """





