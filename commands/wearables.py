from evennia import Command, CmdSet
from evennia import InterruptCommand

class CmdWear(Command):
	"""
	Wear clothes/armor.
	
	Usage:
		wear <clothing/armor name>
	"""
	key = "wear"
	help_category = "Player"

	def parse(self):
		self.args = self.args.strip()
		if not self.args:
			self.caller.msg("Wear what?")
			raise InterruptCommand

	def func(self):
		wearable = self.caller.search(self.args)
		if not wearable:
			return
		try:
			slot = self.obj.db.armor_slot.get()
			wearable.do_wear(self.caller, slot)
		except AttributeError:
			self.caller.msg("You can't wear that!")

class CmdRemove(Command):
	""" 
	Remove clothes/armor
	
	Usage:
		remove <clothing/armor name>
	"""
	key = "remove"


class CmdSetWear(CmdSet):
	def at_cmdset_creation(self):
		self.add(CmdWear())