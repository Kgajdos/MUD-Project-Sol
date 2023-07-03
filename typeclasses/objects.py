"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia import AttributeProperty, DefaultObject, search_object, create_object
from evennia.utils.utils import make_iter
from rules import dice
from utils import get_obj_stats
from enums import WieldLocation, ObjType, Ability



class ObjectParent:
    """
    This is a mixin that can be used to override *all* entities inheriting at
    some distance from DefaultObject (Objects, Exits, Characters and Rooms).

    Just add any method that exists on `DefaultObject` to this class. If one
    of the derived classes has itself defined that same hook already, that will
    take precedence.

    """


class Object(ObjectParent, DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_pre_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_post_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_post_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

    """

    pass


class ProjectSolObject(DefaultObject):
    """
    Base for all evadventure objects.
    """
    inventory_use_slot = WieldLocation.BACKPACK
    size = AttributeProperty(1, autocreate = False)
    value = AttributeProperty(0, autocreate=False)

    # this can be either a single type or a list of types (for objects able to be 
    # act as multiple). This is used to tag this object during creation.
    obj_type = ObjType.GEAR

    #modifying default evennia hooks
    def at_object_creation(self):
        """Called when this object is first created. 
        We convert the .obj_type property to a database tag"""
        for obj_type in make_iter(self.obj_type):
            self.tags.add(self.obj_type.value, category = "obj_type")

    def get_display_header(self, looker, **kwargs):
        """The top of the description"""
        return ""
    
    def get_display_desc(self, looker, **kwargs):
        """The main display - show object stats""" 
        return get_obj_stats(self, owner = looker)
    
    #Custom EvAdventure methods
    def has_obj_type(self, objtype): 
        """Check if object is of a certain type""" 
        return objtype.value in make_iter(self.obj_type)
    
    def at_pre_use(self, *args, **kwargs):
        """Called before use. If returning False, can't be used"""
        return True
    
    def use(self, *args, **kwargs):
        pass

    def post_use(self, *args, **kwargs):
        """Always called post use"""
        pass

    def get_help(self):
        """Get any help text for this item."""
        return "No help for this item"
    

class ProjectSolQuestObject(ProjectSolObject):
    """Quest objects should usually not be possible to sell or trade."""
    obj_type = ObjType.QUEST
 
class ProjectSolTreasure(ProjectSolObject):
    """Treasure is usually just for selling for coin"""
    obj_type = ObjType.LOOT
    value = AttributeProperty(100, autocreate=False)
    

class ProjectSolConsumable(ProjectSolObject):
    """An item that can be used up."""
    obj_type = ObjType.CONSUMABLE
    value = AttributeProperty(0.25, autocreate = False)
    uses = AttributeProperty(1, autocreate=False)

    def at_pre_use(self, user, target=None, *args, **kwargs):
        """Called before using. If returns false, abort."""
        if target and user.location != target.location:
            user.msg("You are not close enough to the target.")
            return False
        
        if self.uses <= 0:
            user.msg(f"|w{self.key} is used up.|n")
            return False
        
    def use(self, user, *args, **kwargs):
        """Called when using the item"""
        pass

    def at_post_use(self, user, *args, **kwargs):
        """Called after using the item""" 
        # detract a usage, deleting the item if used up.
        self.uses -= 1
        if self.uses <= 0: 
            user.msg(f"{self.key} was used up.")
            self.delete()
        
class ProjectSolWeapon(ProjectSolObject): 
    """Base class for all weapons"""

    obj_type = ObjType.WEAPON 
    inventory_use_slot = AttributeProperty(WieldLocation.WEAPON_HAND, autocreate=False)
    quality = AttributeProperty(3, autocreate=False)
    
    attack_type = AttributeProperty(Ability.PHY, autocreate=False)
    defend_type = AttributeProperty(Ability.PHY, autocreate=False)
    
    damage_roll = AttributeProperty("1d6", autocreate=False)


    def at_pre_use(self, user, target=None, *args, **kwargs):
       if target and user.location != target.location:
           # we assume weapons can only be used in the same location
           user.msg("You are not close enough to the target!")
           return False

       if self.quality is not None and self.quality <= 0:
           user.msg(f"{self.get_display_name(user)} is broken and can't be used!")
           return False
       
       return super().at_pre_use(user, target=target, *args, **kwargs)

    def use(self, attacker, target, *args, advantage=False, disadvantage=False, **kwargs):
       """When a weapon is used, it attacks an opponent"""

       location = attacker.location

       is_hit, quality, txt = dice.opposed_saving_throw(
           attacker,
           target,
           attack_type=self.attack_type,
           defense_type=self.defense_type,
           advantage=advantage,
           disadvantage=disadvantage,
       )
       location.msg_contents(
           f"$You() $conj(attack) $You({target.key}) with {self.key}: {txt}",
           from_obj=attacker,
           mapping={target.key: target},
       )
       if is_hit:
           # enemy hit, calculate damage
           dmg = dice.roll(self.damage_roll)

           if quality is Ability.CRITICAL_SUCCESS:
               # doble damage roll for critical success
               dmg += dice.roll(self.damage_roll)
               message = (
                   f" $You() |ycritically|n $conj(hit) $You({target.key}) for |r{dmg}|n damage!"
               )
           else:
               message = f" $You() $conj(hit) $You({target.key}) for |r{dmg}|n damage!"

           location.msg_contents(message, from_obj=attacker, mapping={target.key: target})
           # call hook
           target.at_damage(dmg, attacker=attacker)

       else:
           # a miss
           message = f" $You() $conj(miss) $You({target.key})."
           if quality is Ability.CRITICAL_FAILURE:
                message += ".. it's a |rcritical miss!|n, damaging the weapon."
                if self.quality is not None:
                   self.quality -= 1
                location.msg_contents(message, from_obj=attacker, mapping={target.key: target})

    def at_post_use(self, user, *args, **kwargs):
        if self.quality is not None and self.quality <= 0:
            user.msg(f"|r{self.get_display_name(user)} breaks and can no longer be used!")



class ProjectSolAmor(ProjectSolObject): 
    obj_type = ObjType.ARMOR
    inventory_use_slot = WieldLocation.BODY 

    armor = AttributeProperty(1, autocreate=False)
    quality = AttributeProperty(3, autocreate=False)




class ProjectSolVisor(ProjectSolAmor): 
    obj_type = ObjType.VISOR
    inventory_use_slot = WieldLocation.HEAD

_BARE_HANDS = None

class WeaponBareHands(ProjectSolWeapon):
     obj_type = ObjType.WEAPON
     inventory_use_slot = WieldLocation.WEAPON_HAND
     attack_type = Ability.PHY
     defense_type = Ability.ARMOR
     damage_roll = "1d4"
     quality = None  # let's assume fists are indestructible ...


def get_bare_hands(): 
    """Get the bare hands""" 
    global _BARE_HANDS
    if not _BARE_HANDS: 
        _BARE_HANDS = search_object("Bare hands", typeclass=WeaponBareHands).first()
    if not _BARE_HANDS:
        _BARE_HANDS = create_object(WeaponBareHands, key="Bare hands")
    return _BARE_HANDS