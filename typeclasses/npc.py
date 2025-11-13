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

    def at_char_entered(self, character, **kwargs):
        """
        Called when a character enters the room this NPC is in.
        You can add behavior here if you want.
        """
        pass




class NPCCiveil(NPC):
        def at_object_creation(self):
            super().at_object_creation()
            #tracking what the player has done/asked
            self.db.dialog_flags = {} 
            #populated by loader
            self.db.dialog_tree = {}
            #link to YAML
            self.db.id = "civeil"
            self.key = "Supervisor Civeil"

        def at_char_entered(self, character):
            """
            Called when a character enters the same room.
            We'll trigger the 'intro' dialog if not met yet.
            """
            flags = character.attributes.get("dialog_flags", {})
            if not flags.get("has_met", False):
                self._respond("intro", character)
                flags["has_met"] = True
                character.attributes.add("dialog_flags", flags)

        def msg(self, text=None, from_obj=None, **kwargs):
            """
            React to being spoken to with 'say'
            """
            if from_obj != self:
                try:
                    say_text, is_say = text[0], text[1].get("type") == "say"
                except Exception:
                    is_say = False
                
                if is_say:
                    #evaluate and respond based on keywords
                    self._handle_dialog(say_text, from_obj)
            super().msg(text=text, from_obj=from_obj,**kwargs)

        def _handle_dialog(self, message, speaker):
            """
            Search for dialog trigger keywords in player's message.
            """
            message = message.lower()
            dialog_tree = self.db.dialog_tree or {}
            flags = speaker.attributes.get("dialog_flags", {})

            for topic, node in dialog_tree.items():
                if topic in message:
                    #Handle special hooks like first mission
                    if topic == "intro" and "first_steps" in node:
                        self._trigger_hook("first_steps", speaker)
                    
                    self._respond(topic, speaker)
                    flags[f"asked_{topic}"] = True
                    speaker.attributes.add("dialog_flags", flags)
                    return
            #No matching topic found
            self._respond("fallback", speaker)

        def _respond(self, topic, speaker):
            """
            Respond with text from a dialog node.
            """
            dialog_tree = self.db.dialog_tree or {}
            node = dialog_tree.get(topic)
            if not node:
                return
            text = node.get("text", "").replace("{player}", speaker.key)
            self.execute_cmd(f"say {text}")

        def _trigger_hook(self, hook, speaker):
            """
            Handle one-time effects like assigning the player's ship.
            """
            if hook == "first_steps":
                try:
                    from missions.first_steps import mission_complete
                    mission_complete(speaker)
                except ImportError:
                    speaker.msg("ERROR: Coult not complete onboarding.")

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
        self.msg("The NPC greets you warmly")

class MechanicMenuCommand(Command):
    key="mechanic"
    
    def func(self):
        self.obj.mechanic_shop(self.caller)
