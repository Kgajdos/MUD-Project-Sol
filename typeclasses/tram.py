from evennia import DefaultObject, search_object, TICKER_HANDLER
from typeclasses.objects import Object
from evennia import Command, CmdSet
from evennia import DefaultScript
import random

#Handles Tram object, commands, and scripts

############## COMMANDS BELOW ########################
class CmdEnterTram(Command):
    """
    Entering the tram.

    Usage:
        enter tram

    Only available in the same location as the tram.
    """
    key = "enter tram"
    locks = "cmd:not cmdinside()"

    def func(self):
        tram = self.obj
        self.caller.msg("You board the tram.")
        self.caller.move_to(tram, move_type = "board")

class CmdLeaveTram(Command):
    """
    Leaving the tram.

    Usage:
        leave tram

    Will only be available inside of the tram.
    """
    key = "leave tram"
    locks = "cmd:cmdinside()"

    def func(self):
        tram = self.obj
        parent = tram.location
        self.caller.msg("You disembark the tram.")
        self.caller.move_to(parent, move_type = "disembark")

class CmdSetTram(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdEnterTram())
        self.add(CmdLeaveTram())

############## OBJECTS BELOW ########################
class Tram(Object):

    def at_object_creation(self):
        self.cmdset.add_default(CmdSetTram)
        self.db.driving = False
        #direction the tram is moving (1 forward, -1 backwards)
        self.db.direction = 1
        #The rooms the tram will pass through
        self.scripts.add(TramDrivingScript)
        TICKER_HANDLER.add(60 * 2, self.life_event)

    def create_line(self, station_one, line1, line2, station_two):
        self.db.rooms = [f"#{station_one.id}", f"#{line1.id}", f"#{line2.id}", f"#{station_two.id}"]

    def start_driving(self):
        self.db.driving = True


    def stop_driving(self):
        self.db.driving = False

    def door_call(self):
        open_closed = ""
        if self.db.driving:
            open_closed = "closed"
        else:
            open_closed = "open"

        self.msg_contents(f"The doors {open_closed}.")
    
    def goto_next_room(self):
        currentroom = self.location.dbref
        idx = self.db.rooms.index(currentroom) + self.db.direction

        if idx < 0 or idx >= len(self.db.rooms):
            #Tram reached the end of its path
            self.stop_driving()
            #Reverse now
            self.db.direction *= -1

        else:
            roomref = self.db.rooms[idx]
            room = search_object(roomref)[0]
            self.move_to(room)
            self.msg_contents(f"The tram is moving towards {room.name}.")

    def life_event(self):
        #TODO: Create a random choice that chooses between a list of possible room msgs
        #TODO: Attatch it to a script
        ECHOES = ["Someone coughed.", "A mouse scurries by.", 
                  "Someone sneezed.", "Someone laughs loudly.",
                  "An argument breaks out."]
        msg_echo = random.choice(ECHOES)
        self.msg_contents(msg_echo)


############## SCRIPTS BELOW ########################
class TramDrivingScript(DefaultScript):

    def at_script_creation(self):
        self.key = "tramdriving"
        self.interval = 30
        self.persistent = True
        self.repeats = 0
        self.start_delay = True
        self.start()

    def at_repeat(self):
        if not self.obj.db.driving:
            self.obj.start_driving()
            self.obj.door_call()
            self.obj.goto_next_room()

        else:
            self.obj.stop_driving()
            self.obj.door_call()
