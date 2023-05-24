from typeclasses import merchants
from evennia.scripts.scripts import DefaultScript, Script
from evennia import Objects

#Creating a test merchant 
class Test(Script):
    def unit_test(self):
        merchant1 = evennia.create_object(typeclasses.merchants.NPCMerchant, "Stan S. Stanman")