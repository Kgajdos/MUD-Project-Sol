import evennia 
from evennia import objects, create_object
from typeclasses.objects import Object

class Loot(Object):
	pass


class AmmoCrate(Loot):
	def at_object_creation(self):
		super().at_object_creation()
		self.db.ammo_box_count = 0
		self.db.desc = "A dark green, metal crate with Universal Alliance stamped on the side. It has a max capacity of 100 ammo boxes."


	def load_ammo_crate(self, box):
		if self.db.ammo_box_count == 100:
			self.caller.msg("Ammo crate is full.")
			return
		else:
			box.move_to(self.contents)

	def unload_ammo_crate(self, box, location):
		box.move_to(location.contents)

class AmmoBox(Loot):
	def at_object_creation(self):
		super().at_object_creation()
		self.db.desc = "A dark brown ammo box with Universal Alliance stamped on the side. It can hold 1000 rounds."
		self.db.ammo_count = 1000

	def unload_ammo(self, ammo, caller):
		ammo.move_to(caller.contents)
		if self.db.ammo_count == 0:
			self.delete()


class Ammo(Loot):
	def at_object_creation(self):
		super().at_object_creation()
		self.db.desc = "A common round designed for use with any weapons platform."