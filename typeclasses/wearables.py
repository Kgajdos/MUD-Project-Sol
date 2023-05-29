from evennia import DefaultObject
import random

class Wearable(DefaultObject):
	"""
	A wearable can be defined as anything that the user can place on their body. 

	Each character has a ____.db.worn[armor_slot] attribute to track worn items.

	Armor_Slot: 
	-head
	-body
	-arms
	-feet

	Functions:

	-- set_wearable_slot(self, armor_slot):
			sets the armor to a specified slot. Ex: knife.set_wearable_slot(weapon)

	-- do_wear:
			set's the players __.db.worn[<armor slot>] = <item name> and set's the items self.db.worn = player

	-- do_remove:
			Not properly implemented
	"""
	def at_object_creation(self):
		super().at_object_creation()
		self.db.wearer = None
		self.db.armor_slot = {}

	def set_wearable_slot(self, armor_slot):
		self.db.armor_slot = armor_slot

	def do_wear(self, wearer, wearable):
		"""
		Called when trying to wear this item.
		"""
		current = self.db.wearer
		if current:
			if current == wearer:
				wearer.msg(f"You are already wearing {self.key}.")
			else:
				wearer.msg(f"You can't wear {self.key} " 
				f"- {current} is already wearing that!")
			return
		self.db.wearer = wearer
		slot = wearable.db.armor_slot
		wearer.db.worn[f"{slot}"] = self
		wearer.msg(f"You wear {self.key} on {slot} armor slot.")

	def do_remove(self, remover):
		"""
		Called when trying to remove the object
		"""
		current = self.db.wearer
		if not remover == current:
			remover.msg(f"You are not wearing {self.key}.")
		else:
			self.db.wearer = None
			armor_slot = self.db.armor_slot
			remover.db.worn[armor_slot] = None
			remover.msg(f"You remove {self.key}.")

			

class Armor(Wearable):
	"""
	This is a seperate class to make determining combat power easier.

	Combat power is split into Attack and Defense, Armor needs to handle defense.
	"""
	def at_object_creation(self):
		super().at_object_creation()

class Weapon(Wearable):
	"""
	This is a seperate weapons class that inherits from the wearable class. 
	The only changes made to this class are specific to attack modifiers.
	"""
	def at_object_creation(self):
		super().at_object_creation()
		self.db.wearer = None
		self.db.armor_slot = "hands"
		self.db.weapon = {}
		self.db.modifier = random.randint(1, 10)

	def set_weapon_modifier(self, amount):
		self.db.modifer += amount


	def set_weapon_type(self, type):
		self.db.weapon = type

	def do_wear(self, wielder, weapon):
		"""
		Called when trying to equip a weapon specifically.
		"""
		current = self.db.wearer
		if current:
			if current == wielder:
				wielder.msg(f"You are already wearing {self.key}.")
			else:
				wielder.msg(f"You can't wear {self.key} " 
				f"- {current} is already wearing that!")
			return
		self.db.wearer = wielder
		slot = weapon.db.armor_slot
		wielder.db.worn[f"{slot}"] = self
		wielder.msg(f"You equip {self.key}.")

	def attack(self, target):
	#TODO: This is where a check against the targets physical would need to take place
		if target.db.physical < self.db.damage:
			damage = random.randint(1, 10) + 1
		else:
			damage = 1

		return damage


class Gun(Weapon):

    def at_object_creation(self):
        super().at_object_creation()


