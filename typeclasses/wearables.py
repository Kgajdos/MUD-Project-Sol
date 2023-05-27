from evennia import DefaultObject

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

	-- do_wear:
			set's the players __.db.worn[<armor slot>] = <item name> and set's the items self.db.worn = player

	-- do_remove:
			Not properly implemented
	"""
	def at_object_creation(self):
		super().at_object_creation()
		self.db.wearer = None

	def do_wear(self, wearer, wearable):
		"""
		Called when trying to wear this item.

		Usage:
			wear <item>
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
		print(wearer.db.worn)
		slot = wearable.db.armor_slot
		wearer.db.worn[f"{slot}"] = self
		wearer.msg(f"You wear {self.key} on {slot} armor slot.")

	def do_remove(self, remover, armor_slot):
		"""
		Called when trying to remove the object
		"""
		current = self.db.wearer
		if not remover == current:
			remover.mbs(f"You are not wearing {self.key}.")
		else:
			self.db.wearer = None
			del remover.db.worm[armor_slot]
			remover.msg(f"You remove {self.key}.")

			