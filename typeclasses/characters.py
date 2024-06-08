"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import evennia
from evennia.utils import utils, lazy_property, create
from evennia import DefaultCharacter, AttributeProperty, EvForm, EvTable, scripts
from typeclasses.equipment import EquipmentHandler
from missions.first_steps import mission_setup
from typeclasses.bags import Bag, BagCmdSet
from typeclasses import playerclass
import random
from enums import Ability
from rules import dice
from typeclasses.objects import ObjectParent

class LivingMixin:
    #to make targeting pc easier
    is_pc = False

    @property
    def hurt_level(self):
        """
        String to describe how hurt the character is
        """
        percent = max(0, min(100, 100 * (self.hp / self.hp_max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        elif 80 < percent <= 95:
            return "|gScraped|n"
        elif 60 < percent <= 80:
            return "|gBruised|n"
        elif 45 < percent <= 60:
            return "|yHurt|n"
        elif 30 < percent <= 45:
            return "|yWounded|n"
        elif 15 < percent <= 30:
            return "|rBadly Wounded|n"
        elif 1 < percent <= 15:
            return "|rBarely hanging on|n"
        elif percent == 0:
            return "|rCollapsed!|n"
        
    def heal(self, hp):
        """
        Heal hp amount of health, not exceeding it
        """
        damage = self.hp_max - self.hp
        healed = min(damage, hp)
        self.hp += healed

        self.msg(f"You heal for {healed} HP.")

    def at_pay(self, amount):
        """
        Makes sure we never spend more than we have
        """
        amount = min(amount, self.coins)
        self.credits -= amount
        return amount
    
    def at_attacked(self, attacker, **kwargs):
        """
        Called when being attacked and combat starts
        """
        pass

    def at_damage(self, damage, attacker=None):
        """
        Called when attacking and taking damage
        """
        self.hp -= damage

    def at_defeat(self):
        """
        Called when defeated, traditionally death
        """
        pass

    def at_do_loot(self, looted):
        """
        Called when looting another entity
        """
        looted.at_looted(self)

    def at_looted(self, looter):
        """
        Called when being looted by another.
        """
        #defualt coin to steal
        max_steal = dice.roll("1d10")
        stolen = self.at_pay(max_steal)
        looter.credits += stolen


class Character(LivingMixin, DefaultCharacter):
    """
    (class docstring)
    """
    is_pc = True

    physical = AttributeProperty(random.randint(1, 10))
    mental = AttributeProperty(random.randint(1, 10))
    social = AttributeProperty(random.randint(1, 10))

    hp = AttributeProperty(random.randint(10, 20))
    hp_max = AttributeProperty(hp)
    stamina = AttributeProperty(random.randint(10, 20))

    level = AttributeProperty(1)
    xp = AttributeProperty(0)
    credits = AttributeProperty(0)


    def at_object_creation(self):     
        self.set_player_class()
        self.set_char_description()
        self.tags.add("newbie")

    def set_player_class(self):
        #Determine the player class based on chargen choices
        player_class = self.db.player_class

        # Create an instance of the specific player class based on the value
        if player_class == "Miner":
            playerclass.Miner(self)
        elif player_class == "Freighter":
            playerclass.Freighter(self)
        elif player_class == "Researcher":
            playerclass.Researcher(self)
        elif player_class == "Fighter":
            playerclass.Fighter(self)
        else:
            # Handle unknown or invalid player classes
            pass

    def at_pre_puppet(self, account, session=None, **kwargs):
        if self.tags.has("newbie") and not self.tags.has("tutorial started"):
            mission_setup(self)
        
        super().at_pre_puppet(account, session=session, **kwargs)

    @lazy_property
    def equipment(self):
        return EquipmentHandler(self)
    
    def return_appearance(self, looker):
        """
        The return from this method is what looker sees when looking at this object.
        """
        text = super().return_appearance(looker)
        #Below we need to add the modifiers for how the armor itself looks
        return text

    
        
    #Belo is functions that set a new ship to the player based on their class
    def set_active_ship(self, ship):
        self.db.active_ship = ship

    #Outdated, do not use, will delete when can
    def update_character_on_first_login(self):
        #self.set_char_description()
        #self.set_ship_by_pc_class()
        self.set_stats()
        




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
        self.db.desc = f"Before you stands {self.key}, {pronoun} {adj} {self.db.adjective} and {self.db.body_type} with a {self.db.disposition} disposition."

    #To be called when a character learns a new skill for the first time
    def create_skill_set(self, raw_string):
        skill = self.raw_string


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
        self.credits += credits

    def train_skill(self, skill_trained, amount):
        value = self.attributes.get(skill_trained) * amount
        self.attributes.add(skill_trained, value)
        self.msg(f"You trained {skill_trained} for {value} experience points!")

    #NEEDS THOUROUGH TESTING!!!!
    def player_sheet(self):
        '''
        Takes advantage of the EvForm to create the character sheet.
        '''

        form = EvForm("typeclasses.playerform")
        form.map(cells={1: self.account.key,
                        2: self.key,
                        3: self.db.desc,
                        4: self.mental,
                        5: self.physical,
                        6: self.social,
                        7: self.db.sex})
        # create the EvTables

        health = self.hp
        stamina = self.stamina
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
        
    def at_defeat(self):
        """
        Characters roll on the death table
        """
        if self.location.allow_death:
            #This allows us to have non-lethal rooms
            dice.roll_death(self)
        else:
            self.location.msg_contents("$You() $conj(collapse) in a heap, alive but beaten.")
        
    def at_pre_object_receive(self, moved_object, source_location, **kwargs):
        """Called by Evennia before object arrives 'in' this character."""
        return self.equipment.validate_slot_usage(moved_object)
    
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Called when the object arrives 'in' the character"""
        self.equipment.add(moved_obj)   

    def at_object_leave(self, moved_object, destination, **kwargs):
        """Called by Evennia when object leaves the character"""
        self.equipment.remove(moved_object)

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





