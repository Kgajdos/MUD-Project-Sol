"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""
def sitsonthis(accessing_obj, accessed_obj, *args, **kwargs):
    """
    True if accessing_obj is sitting on/in the accessed_obj.
    """
    return accessed_obj.obj.db.sitter == accessing_obj

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False

def cmdheavy(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage: cmdheavy() 
    Used to lock get commands for heavy items. Subject to change.
    """
    return accessing_obj.msg("It's too heavy")

def cmdweild(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage: cmdweild()
    Used to lock commands to only be available when the item is held.
    """
    return accessing_obj.db.worn["weapon"] == accessed_obj

def cmdinside(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage: cmdinside()
    Used to lock commands and only allows access if the command is defined on 
    an object which accessing_obj is inside of
    """
    return accessed_obj.location == accessing_obj.location

def cmdarmed(accessing_obj, accessed_obj, *args, **kwargs):
    return accessed_obj.location == accessing_obj.contents

def cmdsuperuseronly(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage: cmdsuperuseronly()
    Used to lock commands and only allow access if the account is a superuser.
    """
    pass

def cmdismoving(accessing_ojb, accessed_obj, *args, **kwargs):
    """
    Usage: cmdismoving()
    Used to lock doors if an object is in motion.
    """
    is_not_moving = False

    if not accessed_obj.driving:
        is_not_moving = True

    return is_not_moving

def cmdinstorage(accessing_obj, accessed_obj, *args, **kwargs):
    """
    
    """
    accessing_obj.location == "Hanger" 