from evennia import DefaultScript, create_script, EvTable
from evadventure.rules import dice

class CombatFailure(RuntimeError):
    """If some error happens in combat"""
    pass

class EvAdventureCombatBaseHandler(DefaultScript):
    """
    This should be created when combat starts. It 'ticks' the combat
    and tracks all sides of it.
    """
    action_classes = {}
    fallback_action_dict = {}

    @classmethod
    def get_or_create_combathandler(cls, obj, **kwargs):
        """
        Get or create a combathandler on `obj`.
    
        Args:
            obj (any): The Typeclassed entity to store this Script on. 
        Keyword Args:
            combathandler_key (str): Identifier for script. 'combathandler' by
                default.
            **kwargs: Extra arguments to the Script, if it is created.
    
        """
        if not obj:
            raise CombatFailure("Cannot start combat without a place to do it!")
    
        combathandler_key = kwargs.pop("key", "combathandler")
        combathandler = obj.ndb.combathandler
        if not combathandler or not combathandler.id:
            combathandler = obj.scripts.get(combathandler_key).first()
            if not combathandler:
                # have to create from scratch
                persistent = kwargs.pop("persistent", True)
                combathandler = create_script(
                    cls,
                    key=combathandler_key,
                    obj=obj,
                    persistent=persistent,
                    **kwargs,
                )
            obj.ndb.combathandler = combathandler
        return combathandler

    def msg(self, message, combatant=None, broadcast=True, location=True):
        """ 
        Central place for sending messages to combatants. This allows
        for adding any combat-specific text-decoration in one place.

        Args:
            message (str): The message to send.
            combatant (Object): The 'You' in the message, if any.
            broadcast (bool): If `False`, `combatant` must be included and
                will be the only one to see the message. If `True`, send to
                everyone in the location.
            location (Object, optional): If given, use this as the location to
                send broadcast messages to. If not, use `self.obj` as that
                location.

        Notes:
            If `combatant` is given, use `$You/you()` markup to create
            a message that looks different depending on who sees it. Use
            `$You(combatant_key)` to refer to other combatants.
        
    	""" 
        if not location:
            location = self.obj

        location_objs = location.contents

        exclude = []

        if not broadcast and combatant:
            exclude = [obj for obj in location_objs if obj is not combatant]

        location.msg_contents(
            message,
            exclude=exclude,
            from_obj=combatant,
            mapping={locobj.key: locobj for locobj in location_objs}
        )

    def get_combat_summary(self, combatant):
        """ 
        Get a nicely formatted 'battle report' of combat, from the 
        perspective of the combatant.
        
    	""" 
        allies, enemies = self.get_sides(combatant)
        #We must include ourselves at the top of the list
        allies.insert(0, combatant)
        nallies, nenemies = len(allies), len(enemies)

        #preparing colors and hurt levels
        allies = [f"{ally} ({ally.hurt_level})" for ally in allies]
        enemies = [f"{enemy} {enemy.hurt_level})" for enemy in enemies]

        #The center collumn with the vs
        vs_column = ["" for _ in range(max(nallies, nenemies))]
        vs_column[len(vs_column) // 2] = "|wvs|n"

        #Two allies and enemy columns should be centered vertically
        diff = abs(nallies - nenemies)
        top_empty = diff // 2
        bot_empty = diff - top_empty
        topfill = ["" for _ in range(top_empty)]
        botfill = ["" for _ in range(bot_empty)]

        if nallies >= nenemies:
            enemies = topfill + enemies + botfill
        else:
            allies = topfill + allies + botfill

        #Make a table with three columns
        return EvTable(
            table=[
                EvTable.EvColumn(*allies, align="l"),
                EvTable.EvColumn(*vs_column, align="c"),
                EvTable.EvColumn(*enemies, align="r")
            ],
            border = None,
            maxwidth = 78
        )


	# implemented differently by Twitch- and Turnbased combat

    def get_sides(self, combatant):
        """ 
        Get who's still alive on the two sides of combat, as a 
        tuple `([allies], [enemies])` from the perspective of `combatant` 
	        (who is _not_ included in the `allies` list.
        
        """
        raise NotImplementedError 

    def give_advantage(self, recipient, target): 
        """ 
        Give advantage to recipient against target.
        
        """
        raise NotImplementedError 

    def give_disadvantage(self, recipient, target): 
        """
        Give disadvantage to recipient against target. 

        """
        raise NotImplementedError

    def has_advantage(self, combatant, target): 
        """ 
        Does combatant have advantage against target?
        
        """ 
        raise NotImplementedError 

    def has_disadvantage(self, combatant, target): 
        """ 
        Does combatant have disadvantage against target?
        
        """ 
        raise NotImplementedError

    def queue_action(self, combatant, action_dict):
        """ 
        Queue an action for the combatant by providing 
        action dict.
        
        """ 
        raise NotImplementedError

    def execute_next_action(self, combatant): 
        """ 
        Perform a combatant's next action.
        
        """ 
        raise NotImplementedError

    def start_combat(self): 
        """ 
        Start combat.
        
    	""" 
        raise NotImplementedError
    
    def check_stop_combat(self): 
        """
        Check if the combat is over and if it should be stopped.
         
        """
        raise NotImplementedError 
        
    def stop_combat(self): 
        """ 
        Stop combat and do cleanup.
        
        """
        raise NotImplementedError   
    
class CombatAction:
    def __init__(self, combathandler, combatant, action_dict):
        self.combathandler = combathandler
        self.combatant  = combatant

        for key, val in action_dict.items():
            if key.startswith("_"):
                setattr(self, key, val)

    def msg(self, message, broadcast=True):
        "Send message to others in combat"
        self.combathandler.msg(message, combatant=self.combatant, broadcast=broadcast)

    def can_use(self): 
        """Return False if combatant can's use this action right now""" 
        return True 

    def execute(self): 
        """Does the actional action"""
        pass

    def post_execute(self):
        """Called after `execute`"""
        pass 


class CombatActionHold(CombatAction):
    """
    Action that does nothing

    action_dict = {"key": "hold"}
    """
    pass

class CombatActionAttack(CombatAction):
    """
    A regular attack, using a wielded weapon.

    action_dict = {
            "key": "attack",
            "target": character/object
    }
    """
    def execute(self):
        attacker = self.combatant
        weapon = attacker.weapon
        target = self.target

        if weapon.at_pre_use(attacker, target):
            weapon.use(
                attacker, target, advantage=self.combathandler.has_advantage(attacker, target)
            )
            weapon.at_post_use(attacker, target)


class CombatActionStunt(CombatAction):
    """
    Perform a stunt the grants a beneficiary (can be self) advantage on their next action against a 
    target. Whenever performing a stunt that would affect another negatively (giving them
    disadvantage against an ally, or granting an advantage against them, we need to make a check
    first. We don't do a check if giving an advantage to an ally or ourselves.

    action_dict = {
           "key": "stunt",
           "recipient": Character/NPC,
           "target": Character/NPC,
           "advantage": bool,  # if False, it's a disadvantage
           "stunt_type": Ability,  # what ability (like STR, DEX etc) to use to perform this stunt. 
           "defense_type": Ability, # what ability to use to defend against (negative) effects of
            this stunt.
        }

    """

    def execute(self):
        combathandler = self.combathandler
        attacker = self.combatant
        recipient = self.recipient  # the one to receive the effect of the stunt
        target = self.target  # the affected by the stunt (can be the same as recipient/combatant)
        txt = ""

        if recipient == target:
            # grant another entity dis/advantage against themselves
            defender = recipient
        else:
            # recipient not same as target; who will defend depends on disadvantage or advantage
            # to give.
            defender = target if self.advantage else recipient

        # trying to give advantage to recipient against target. Target defends against caller
        is_success, _, txt = dice.opposed_saving_throw(
            attacker,
            defender,
            attack_type=self.stunt_type,
            defense_type=self.defense_type,
            advantage=combathandler.has_advantage(attacker, defender),
            disadvantage=combathandler.has_disadvantage(attacker, defender),
        )

        self.msg(f"$You() $conj(attempt) stunt on $You({defender.key}). {txt}")

        # deal with results
        if is_success:
            if self.advantage:
                combathandler.give_advantage(recipient, target)
            else:
                combathandler.give_disadvantage(recipient, target)
            if recipient == self.combatant:
                self.msg(
                    f"$You() $conj(gain) {'advantage' if self.advantage else 'disadvantage'} "
                    f"against $You({target.key})!"
                )
            else:
                self.msg(
                    f"$You() $conj(cause) $You({recipient.key}) "
                    f"to gain {'advantage' if self.advantage else 'disadvantage'} "
                    f"against $You({target.key})!"
                )
            self.msg(
                "|yHaving succeeded, you hold back to plan your next move.|n [hold]",
                broadcast=False,
            )
        else:
            self.msg(f"$You({defender.key}) $conj(resist)! $You() $conj(fail) the stunt.")

class CombatActionUseItem(CombatAction):
    """
    Use an item in combat. This is meant for one-off or limited-use items (so things like scrolls and potions, not swords and shields). If this is some sort of weapon or spell rune, we refer to the item to determine what to use for attack/defense rolls.

    action_dict = {
            "key": "use",
            "item": Object
            "target": Character/NPC/Object/None
        }

    """

    def execute(self):
        item = self.item
        user = self.combatant
        target = self.target

        if item.at_pre_use(user, target):
            item.use(
                user,
                target,
                advantage=self.combathandler.has_advantage(user, target),
                disadvantage=self.combathandler.has_disadvantage(user, target),
            )
            item.at_post_use(user, target)

class CombatActionWield(CombatAction):
    """
    Wield a new weapon (or spell) from your inventory. This will 
	    swap out the one you are currently wielding, if any.

    action_dict = {
            "key": "wield",
            "item": Object
        }

    """

    def execute(self):
        self.combatant.equipment.move(self.item)