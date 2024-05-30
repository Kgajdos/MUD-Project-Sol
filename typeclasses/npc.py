from typeclasses.characters import Character
from evennia import Command, CmdSet, EvMenu
from typeclasses.ships import ShipManager
from typeclasses.objects import Object

#This needs Fixed!!
class MechanicNPC(Character):
    def at_object_creation(self):
        self.cmdset.add_default(MechanicCommandSet)


    def spawn_ship(self):
        player = self.caller
        player_class = player.db.player_class
        if not player_class:
            pass #TODO: Probably need to handle this a little better
        ship = self.spawn_ship(player_class)
        return ship
    
    def mechanic_shop(self, player):
        menunodes = {
            "menunode_start": menunode_start,
        }
        shopname = self.db.name or "Mechanic"
        EvMenu(player, menunodes, startnode = "menunode_start",
               shopname = shopname, shopkeeper = self)
    


#########################################################################
# MECHANIC EVMENU 
#########################################################################
def menunode_start(caller):
    menu = caller.nbd._evmenu
    shopkeeper = menu.shopkeeper
    player = menu.player
    text = f"Welcome {player.key}!\nHow can I help you?"
    options = [{
        "desc": f"|cAsk about ship|n", "goto": "menunode_ship",
    }]
    return text, options

def menunode_ship(caller, raw_string, **kwargs):
    menu = caller.nbd._evmenu
    player = menu.player
    player_ship = player.db.player_class
    if not player_ship:
        return
    text = "Here you go!"
    return text



class NPC(Character):
    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add_default(NPCCommandSet())

    def at_char_entered(self, character):
        character.msg(f"Greetings, {character.key}. How can I assist you?")

class MechanicCommandSet(CmdSet):
    key = "mechaniccmdset"
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(MechanicMenuCommand())

class NPCCommandSet(CmdSet):
    key = "npccmdset"
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdGreet())

class CmdGreet(Command):
    key = "greet"
    aliases = ["hello", "hi"]
    help_category = "General"

    def func(self):
        self.caller.msg("The NPC greets you warmly")

class MechanicMenuCommand(Command):
    key="mechanic"
    
    def func(self):
        self.obj.mechanic_shop(self.caller)
