import evennia
from evennia import DefaultObject
from evennia import create_object, search_object

#HEADER
#This is a batch code vs of the build kuiper station
market_floor = create_object("typeclasses.rooms.Room", key = "Market Floor 1", aliases = "floor1")
#
hanger = create_object("typeclasses.rooms.Room", key = "Ship Hanger", aliases = "hanger", location = "Market Floor 1")
#
hallway = create_object("typeclasses.rooms.Room", key = "Public Hallway", aliases = "hallway", location = "Market Floor 1")
#
clothes = create_object("typeclasses.rooms.Room", key = "Rev's Emporium", aliases = "clothing", location = "Market Floor 1")
#
guns = create_object("typeclasses.rooms.Room", key = "Basic Space Gun Shop", aliases = "gunshop", location = "Market Floor 1")
#
station = create_object("typeclasses.rooms.Room", key = "Public Hallway", aliases = "hallway", location = "Market Floor 1")