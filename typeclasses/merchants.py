from typeclasses.objects import Object
from world.prototypes import MERCHANT_TYPES, GENERAL_MERCHANT_WARES, FOODRINK_MERCHANT_WARES, ARMORER_MERCHANT_WARES,   SHIPS_MERCHANT_WARES
from typeclasses.rooms import Room
from typeclasses.corporations import Corporation
from evennia import prototypes, AttributeProperty, utils, Command, CmdSet, EvMenu, InterruptCommand, DefaultScript, search_object, typeclasses, TICKER_HANDLER
import random, datetime
from data import resources


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


#This set of nodes is used for players selling cargo based goods
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
        credit_val = ware.db.value or 1
        options.append({"desc": (f"{ware.key} {credit_val} credits"),
                        "goto": ("inspect_and_buy", 
                                 {"selected_ware": ware})
                       })
    options.append({"desc": (f"Sell"),
                    "goto": ("sell_page")})
                       
    return text, options

def _buy_item(caller, raw_string, **kwargs):
    "Called if player chooses to buy"
    ware = kwargs["selected_ware"]
    selected_ware = search_object(ware)
    value = selected_ware[0].db.value or 1
    wealth = caller.credits or 0

    if wealth >= value:
        rtext = f"You pay {value} credits and purchase {selected_ware[0].key}!"
        caller.credits -= int(value)
        selected_ware[0].move_to(caller.contents)
    else:
        rtext = f"You cannot afford {value} credits for {selected_ware[0].key}!"
    caller.msg(rtext)
    # no matter what, we return to the top level of the shop
    return "shopfront"

def node_inspect_and_buy(caller, raw_string, **kwargs):
    "Sets up the buy menu screen."
    ware = kwargs["selected_ware"]

    selected_ware = search_object(ware)
    value = selected_ware[0].db.value or 1

    text = f"You inspect {selected_ware[0].key}:\n\n{selected_ware[0].db.desc}"

    options = ({
            "desc": f"Buy {selected_ware[0].key} for {value} credits",
            "goto": (_buy_item, kwargs)
        }, {
            "desc": "Look for something else",
            "goto": "shopfront",
        })
    return text, options

def sell_page(caller, raw_string, **kwargs):
    text = {}
    ship = caller.active_ship()

    if ship == None:
        caller.msg("Something went wrong, do you have an active ship?")
        return "shopfront"
    
    wares = ship.check_cargo()
    for item, quantity in wares.items():
        text[item] = int(quantity)

    options = []
    for ware, quantity in wares.items():
        if not ware:
            continue

        res_ware = ware.upper()
        resource_data = getattr(resources, res_ware, None)
        if resource_data:
            credit_val = resource_data.get("value", 1)
            payout = int(credit_val) * int(quantity)
            options.append({"desc": (f"{res_ware} - {payout} credits"),
                            "goto": (_sell, 
                                    {"selected_ware": res_ware})
                        })
    return text, options
    
def _sell(caller, raw_string, **kwargs):
    selected_ware = kwargs["selected_ware"]
    resource = getattr(resources, selected_ware, None)
    menu = caller.ndb._evmenu
    shopkeeper = menu.shopkeeper 

    if not resource:
        caller.msg("Something went wrong. That resource can't be sold.")
        return "shopfront"
    
    ship = caller.active_ship()

    if ship == None:
        caller.msg("Something went wrong, do you have an active ship?")
        return "shopfront"
    
    cargo = ship.check_cargo()
    quantity = cargo.get(selected_ware.lower(), 0)

    if int(quantity) <= 0:
        caller.msg("You don't have any of that to sell.")
        return "shopfront"
    value_per_unit = resource.get("value", 1)
    total_value = int(value_per_unit) * int(quantity)
    ship.remove_cargo(selected_ware.lower())

    try:
        caller.add_credits(int(total_value))
        corp = shopkeeper.attributes.get("corp")
        corp = search_object(corp)
        corp[0].add_to_reserves(resource = {selected_ware: int(quantity)})
    except Exception as e:
        utils.logger.log_err(e, **kwargs)
        caller.msg("Something went wrong while adding your credits.")

    return "shopfront"

#This set of nodes is used when the player trades research points for goods
def node_tradefront(caller, raw_string, **kwargs):
    "This is the top-menu screen."

     # made available since we passed them to EvMenu on start 
    menu = caller.ndb._evmenu
    shopname = menu.shopname
    shopkeeper = menu.shopkeeper 
    wares = shopkeeper.contents

    text = f"*** Welcome to {shopname}! ***\n"
    if wares:
        text += f"   Things for trade (choose 1-{len(wares)} to inspect); quit to exit:"
    else:
        text += "   There is nothing to trade right now; quit to exit."

    options = []
    for ware in wares:
         # add an option for every ware in store
        searched_ware = search_object(ware)
        research_val = searched_ware[0].db.value or 1
        options.append({"desc": (f"{ware.key} {research_val} research points"),
                        "goto": ("inspect_and_trade", 
                                 {"selected_ware": ware})
                       })
                       
    return text, options

def node_inspect_and_trade(caller, raw_string, **kwargs):
    "Sets up the trade menu screen."

        # passed from the option we chose 
    ware = kwargs["selected_ware"]
    selected_ware = search_object(ware)
    value = selected_ware[0].db.value or 1
    text = f"You inspect {selected_ware[0].key}:\n\n{selected_ware[0].db.desc}"

    options = ({
            "desc": f"Trade {selected_ware[0].key} for {value} research points",
            "goto": (_trade_item, kwargs)
        }, {
            "desc": "Look for something else",
            "goto": "tradefront",
        })
    return text, options

def _trade_item(caller, raw_string, **kwargs):
    "Called if player chooses to trade."
    ware = kwargs["selected_ware"]
    selected_ware = search_object(ware)
    value = selected_ware[0].db.research_value or 1
    ship = caller.active_ship()

    if ship == None:
        caller.msg("Something went wrong, do you have an active ship?")
        return "tradefront"
    
    availablepoints = 0
    for item, quantity in ship.db.cargo.items():
        if item == "research":
            availablepoints = quantity

    if availablepoints >= value:
        rtext = f"You trade {value} research points and purchase {selected_ware[0].key}!"
        ship.db.cargo["research"] -= value
        selected_ware[0].move_to(caller)
        
    else:
        rtext = f"You do not have {value} research points for {selected_ware[0].key}!"
    caller.msg(rtext)
    # no matter what, we return to the top level of the shop
    return "tradefront"

class NPCMerchant(Object):

    def at_object_creation(self):
        self.db.inventory = {}
        self.db.last_restock = datetime.datetime.now()
        self.attributes.add("corp", None)
        self.attributes.add("merchant_type", None)
        self.cmdset.add_default(MerchantCmdSet)
        TICKER_HANDLER.add(60 * 2, self.dialog)
        TICKER_HANDLER.add(60 * 24, self.restock_items)

    def restock_items(self):
        now = datetime.datetime.now()
        self.location.msg_contents(f"{self.key} turns to face a currier.")
        merchant_type = self.attributes.get("merchant_type")
        if now - self.db.last_restock >= datetime.timedelta(hours=24):
            self.location.msg_contents(f"{self.key} recieves a package.")
            match merchant_type:
                case "General":
                    try:
                        for item in GENERAL_MERCHANT_WARES:
                            proto = prototypes.spawner.spawn(item)
                            proto[0].move_to(self)
                            self.db.last_restock = datetime.datetime.now()
                    except Exception as e:
                        print(f"{e}")
                case "FooDrink":
                    try:
                        for item in FOODRINK_MERCHANT_WARES:
                            proto = prototypes.spawner.spawn(item)
                            proto[0].move_to(self)
                            self.db.last_restock = datetime.datetime.now()
                    except Exception as e:
                        print(f"{e}")
                case "Armorer":
                    try:
                        for item in ARMORER_MERCHANT_WARES:
                            proto = prototypes.spawner.spawn(item)
                            proto[0].move_to(self)
                            self.db.last_restock = datetime.datetime.now()
                    except Exception as e:
                        print(f"{e}")
                case "Ships":
                    pass
        else:
            self.location.msg_contents(f"{self.key} turns away.")

    def open_shop(self, shopper):
        menunodes = {
            "shopfront": node_shopfront,
            "inspect_and_buy": node_inspect_and_buy,
            "sell_page": sell_page
        } 
        shopname = self.db.shopname or "The shop"
        EvMenu(shopper, menunodes, startnode = "shopfront", 
               shopname = shopname, shopkeeper = self, wares = self.contents)
        
    def dialog(self):
        ECHOES = ["Every pilot needs a ship!", "Have you checked out my shop yet?",
                  "Let Basic Space fulfull your needs.", "Remember that space is dangerous!",
                  "Everything you sell benefits the corp."]
        msg_echo = random.choice(ECHOES)
        self.location.msg_contents(msg_echo)

class NPCResearchMerchant(NPCMerchant):
    """
    A specific type of merchant that only takes research points as payment.
    """
    def at_object_creation(self):
        self.attributes.add("corp", None)
        self.cmdset.add_default(MerchantCmdSet)
        TICKER_HANDLER.add(60 * 2, self.dialog)

    def dialog(self):
        ECHOES = ["Exchange your valuable research for goods here!", "Buying your research!",
                  "Your corporation thanks you.", "All research benefits the corp.",
                  "The answers are among the stars."]
        msg_echo = random.choice(ECHOES)
        self.location.msg_contents(msg_echo)

    def open_shop(self, shopper):
        menunodes = {
            "tradefront": node_tradefront,
            "inspect_and_trade": node_inspect_and_trade
        }
        shopname = f"{self.key}'s Reasearch Station"
        EvMenu(shopper, menunodes, startnode = "tradefront",
               shopname = shopname, shopkeeper = self, wares = self.contents)
        

class MerchantPassiveDialog(Object):
    #This only exists to get my server to stop yelling at me.
    #TODO: figure out why the server is expecting this class.
    def is_active(self): #Server expects this
        pass