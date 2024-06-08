from typeclasses.contract import ContractHandler
from typeclasses.ships import ShipManager

def mission_setup(player):
    player_class = player.db.player_class
    player.tags.add("tutorial started")
    ship = ShipManager.spawn_ship(player_class)
    first_steps = ContractHandler.create_job("Visit Civeil for your first ship.", ship, "Find Civeil.", None)
    if not player.db.missions:
        player.db.missions = []
    player.db.missions.append("first steps")
    player.set_active_ship(ship)
    ship.db.pilot = player
    player.msg("You hear a strong voice shouting from the other room.\n 'Out here!'")

def mission_complete(self, player, ship):
    #TODO: Finish mission logic
    player.tags.remove("newbie")
    player.tags.remove("tutorial started")
    player.tags.add("captain")

