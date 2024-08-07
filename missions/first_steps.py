from typeclasses.contract import ContractHandler
from typeclasses.ships import ShipManager
from evennia import utils

def mission_setup(player):

    player_class = player.db.player_class
    player.tags.add("tutorial started")
    ship = ShipManager.spawn_ship(player_class)
    ship.move_to(player.search("#431")) #this needs to be changed based on wherever the space hanger is located!
    player.set_active_ship(ship.db.shipid)
    ship.db.pilot = player
    mission_start(player)
    
    if not isinstance(player.db.missions, list):
        player.db.missions = []



def mission_start(player): 
    player.msg("Go visit Civeil in the Hangers, there is a map on the wall in this room.")
    utils.delay(3, tutorial_step1, player)

def tutorial_step1(player):
    player.msg("To check out your surroundings, type in look and press Enter.")
    utils.delay(3, tutorial_step2, player)

#UPDATE THIS!!! Base it off of the map structure, for now, go north
def tutorial_step2(player):
    player.msg("There's a door to the north. Why don't you step through it. Type north (n) and press Enter.")

def mission_complete(player):
    if "first steps" in player.db.missions:
        player.db.missions.remove("first steps")
    player.tags.remove("tutorial started")
    player.tags.add("captain")
    player.msg("Congratulations! You've completed the tutorial and are now a captain.")

