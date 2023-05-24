from evennia import typeclasses, TICKER_HANDLER
from typeclasses.objects import Object
from typeclasses.rooms import Room
from evennia import Command, CmdSet, EvMenu
from evennia import InterruptCommand
from evennia import DefaultScript
import random


class CmdOpenShop(Command):
    """
    Open the shop!

    Usage:
        shop/buy

    """
    key = "shop"
    aliases = ["buy"]
    help_category = "General"

    def func(self):
        #merchant is self.obj
        #self.caller is pc
        self.obj.open_shop(self.caller)

class MerchantCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdOpenShop())



def node_shopfront(caller, raw_string, **kwargs):
    "This is the top-menu screen."

     # made available since we passed them to EvMenu on start 
    menu = caller.ndb._evmenu
    shopname = menu.shopname
    shopkeeper = menu.shopkeeper 
    wares = shopkeeper.contents

    text = f"*** Welcome to {shopname}! ***\n"
    if wares:
        text += f"   Things for sale (choose 1-{len(wares)} to inspect); quit to exit:"
    else:
        text += "   There is nothing for sale; quit to exit."

    options = []
    for ware in wares:
         # add an option for every ware in store
        credit_val = ware.db.credit_value or 1
        options.append({"desc": (f"{ware.key} {credit_val} credits"),
                        "goto": ("inspect_and_buy", 
                                 {"selected_ware": ware})
                       })
                       
    return text, options

def _buy_item(caller, raw_string, **kwargs):
    "Called if buyer chooses to buy"
    selected_ware = kwargs["selected_ware"]
    value = selected_ware.db.credit_value or 1
    wealth = caller.db.credit or 0

    if wealth >= value:
        rtext = f"You pay {value} credits and purchase {selected_ware.key}!"
        caller.db.credit -= value
        newship = selected_ware.copy(new_key = "Player Ship")
        newship.move_to(caller, quiet=True, move_type="buy")
    else:
        rtext = f"You cannot afford {value} credits for {selected_ware.key}!"
    caller.msg(rtext)
    # no matter what, we return to the top level of the shop
    return "shopfront"

def node_inspect_and_buy(caller, raw_string, **kwargs):
    "Sets up the buy menu screen."

        # passed from the option we chose 
    selected_ware = kwargs["selected_ware"]

    value = selected_ware.db.credit_value or 1
    text = f"You inspect {selected_ware.key}:\n\n{selected_ware.db.desc}"

    options = ({
            "desc": f"Buy {selected_ware.key} for {value} gold",
            "goto": (_buy_item, kwargs)
        }, {
            "desc": "Look for something else",
            "goto": "shopfront",
        })
    return text, options

class NPCMerchant(Object):

    def at_object_creation(self):
        self.cmdset.add_default(MerchantCmdSet)
        TICKER_HANDLER.add(60 * 2, self.dialog)

    def open_shop(self, shopper):
        menunodes = {
            "shopfront": node_shopfront,
            "inspect_and_buy": node_inspect_and_buy
        } 
        shopname = self.db.shopname or "The shop"
        EvMenu(shopper, menunodes, startnode = "shopfront", 
               shopname = shopname, shopkeeper = self, wares = self.contents)
        
    def dialog(self):
        ECHOES = ["Every pilot needs a ship!", "Have you checked out my shop yet?",
                  "Let Basic Space fulfull your needs.", "Remember that space is dangerous!"]
        msg_echo = random.choice(ECHOES)
        self.location.msg_contents(msg_echo)


class MerchantPassiveDialog(Object):
    #This only exists to get my server to stop yelling at me.
    #TODO: figure out why the server is expecting this class.
    def is_active(self): #Server expects this
        pass