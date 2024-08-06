from typeclasses.characters import Character
from typeclasses.ships import ShipManager
from evennia import Command, CmdSet, EvMenu, AttributeProperty, create_object



    


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

    is_pc = False

    def at_object_creation(self):
        super().at_object_creation()
        self.cmdset.add(NPCCommandSet, persistent=True)



class NPCCiveil(NPC):
        def at_object_creation(self):
            super().at_object_creation()

        def at_char_entered(self, character):
            if character.tags.has("captain"):
                character.msg(f"{self.key} says: How's the {character.db.active_ship.key} treating you?")
            else:
                from missions.first_steps import mission_complete
                mission_complete(character)
                character.msg(f"{self.key} says: Greetings, {character.key}. Are you here for your ship?")

        def msg(self, text=None, from_obj=None, **kwargs):
            "Custom msg() method reacting to say."
            if from_obj != self:
                # make sure to not repeat what we ourselves said or we'll create a loop
                try:
                    # if text comes from a say, `text` is `('say_text', {'type': 'say'})`
                    say_text, is_say = text[0], text[1]['type'] == 'say'
                except Exception:
                    is_say = False
                if is_say:
                    # First get the response (if any)
                    response = f"Ah hello {from_obj}! I've been waiting for you."
                    # If there is a response
                    if response != None:
                        # speak ourselves, using the return
                        self.execute_cmd(f"say {response}")   

        
            # this is needed if anyone ever puppets this NPC - without it you would never
            # get any feedback from the server (not even the results of look)
                super().msg(text=text, from_obj=from_obj, **kwargs) 

        

#This needs Fixed!!
class MechanicNPC(NPC):
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
# Commands
#########################################################################        

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
