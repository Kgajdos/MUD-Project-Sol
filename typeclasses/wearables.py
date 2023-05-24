from evennia import DefaultObject

class Wearable(DefaultObject):
	def at_object_creation(self):
		super().at_object_creation()
		self.db.wearer = None

	def do_wear(self, wearer, armor_slot):
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
				f"- {current.key} is already wearing that!")
			return
		self.db.wearer = wearer
		wearer.db.worn[f"{armor_slot}"] = self
		wearer.msg(f"You wear {self.key} on {armor_slot} armor slot.")

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

			