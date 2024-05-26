"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

For example, you might have a Sword typeclass that implements everything a
Sword would need to do. The only difference between different individual Swords
would be their key, description and some Attributes. The Prototype system
allows to create a range of such Swords with only minor variations. Prototypes
can also inherit and combine together to form entire hierarchies (such as
giving all Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a hierarchy of
typeclasses instead.

A prototype can either be a dictionary placed into a global variable in a
python module (a 'module-prototype') or stored in the database as a dict on a
special Script (a db-prototype). The former can be created just by adding dicts
to modules Evennia looks at for prototypes, the latter is easiest created
in-game via the `olc` command/menu.

Prototypes are read and used to create new objects with the `spawn` command
or directly via `evennia.spawn` or the full path `evennia.prototypes.spawner.spawn`.

A prototype dictionary have the following keywords:

Possible keywords are:
- `prototype_key` - the name of the prototype. This is required for db-prototypes,
  for module-prototypes, the global variable name of the dict is used instead
- `prototype_parent` - string pointing to parent prototype if any. Prototype inherits
  in a similar way as classes, with children overriding values in their parents.
- `key` - string, the main object identifier.
- `typeclass` - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
- `location` - this should be a valid object or #dbref.
- `home` - valid object or #dbref.
- `destination` - only valid for exits (object or #dbref).
- `permissions` - string or list of permission strings.
- `locks` - a lock-string to use for the spawned object.
- `aliases` - string or list of strings.
- `attrs` - Attributes, expressed as a list of tuples on the form `(attrname, value)`,
  `(attrname, value, category)`, or `(attrname, value, category, locks)`. If using one
   of the shorter forms, defaults are used for the rest.
- `tags` - Tags, as a list of tuples `(tag,)`, `(tag, category)` or `(tag, category, data)`.
-  Any other keywords are interpreted as Attributes with no category or lock.
   These will internally be added to `attrs` (equivalent to `(attrname, value)`.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.

"""

## example of module-based prototypes using
## the variable name as `prototype_key` and
## simple Attributes
import evennia

#BS Armor line - for use as beginner equipment



ROOM_BRIDGE = {
    "prototype_key": "ROOM_BRIDGE",
    "key": "Bridge",
    "typeclass": "typeclasses.rooms.Room",
    "attrs": [("desc","You stand at the bridge of your ship. It is only large enough for around three people to comfortably be in. There is a Captain's chair made of soft leather and an older console in front of you.")]
    }



RAT_ENEMY = {
    "prototype_key": "RAT_ENEMY",
    "key": "Rat",
    "typeclass": "typeclasses.enemies.Enemy",
    "attrs": [("desc", "A small, angry looking rat.")]
}

ROOM_QUARTERS = {
    "key": "Quarters",
    "typeclass": "typeclasses.rooms.Room",
    "contents": "bed_prototype"
}

ROOM_STORAGE = {
    "key": "Storage",
    "typeclass": "typeclasses.rooms.Room"
}


CONSOLE = {
    "key": "Console",
    "typeclass": "typeclasses.ships.ShipConsole"
}

CAPCHAIR = {
    "key": "Captain's Chair",
    "typeclass": "typeclasses.sittables.Sittable"
}

#TODO: Create a bed class, give it sittables cmds and layables/sleep commands
BED = {
    "key": "Bed",
    "typeclass": "typeclasses.objects.Object",
    "attribute": {"desc": "A small, warm looking bed with soft sheets and a large blanket."},
    "tags": [("furniture")]

}
