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

NPC_CIVEIL = {
    "prototype_key": "NPC_CIVEIL",
    "key": "Civeil",
    "typeclass": "typeclasses.npc.NPC",
    "attrs": [("desc", "Before you stands a woman with advanced cybernetics to include eyes and an arm. Her hair is strikingly white. It is impossible to determine her age beyond 'older than you'. She stands in front of a computer ready to assist.")]
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

BS_HELMET = {
    "prototype_key": "BS_HELMET",
    "key": "BS Helmet",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["helmet"],
    "attrs": [("desc", "A helmet made by Basic Space. Are those dents?"),
              ("armor_slot", "head"),
              ("quality", 'POOR')],
}

BS_SUIT = {
    "prototype_key": "BS_SUIT",
    "key": "BS Suit",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["suit"],
    "attrs": [("desc", "A space suit designed by Basic Space. I'm sure that's not a stain."),
              ("armor_slot", "body"),
              ("quality", 'POOR')],
}

BS_GLOVES = {
    "prototype_key": "BS_GLOVES",
    "key": "BS Gloves",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["gloves"],
    "attrs": [("desc", "Gloves made by Basic Space. Hopefully your fingers won't freeze out there."),
              ("armor_slot", "arms"),
              ("quality", 'POOR')],
}

BS_BOOTS = {
    "prototype_key": "BS_BOOTS",
    "key": "BS Boots",
    "value": 100,
    "typeclass": "typeclasses.wearables.Armor",
    "aliases": ["boots"],
    "attrs": [("desc", "Boots designed by Basic Space. They don't look very comfortable."),
              ("armor_slot", "feet"),
              ("quality", 'POOR')],
}

BS_RIFLE = {
    "prototype_key": "BS_RIFLE",
    "key": "BS Rifle",
    "value": 100,
    "aliases": ["riffle"],
    "typeclass": "typeclasses.weapons.Gun",
    "attrs": [("desc", "A rifle designed by Basic Space. It seems kind of light and flimsy."),
              ("armor_slot", "hands"),
              ("quality", 'POOR')],
}

BS_DRINK = {
    "prototype_key": "BS_DRINK",
    "key": "BS Drink",
    "value": 10,
    "typeclass": "typeclasses.drinkables.Drinkables",
    "attrs": [("desc", "A drink designed by Basic Space. The taste is awful, but promises improved focus!"),
              ("quality",'POOR'),
              ("effects", {"mental": 0.01})],
}

BS_STEW = {
    "prototype_key": "BS_STEW",
    "key": "BS Stew",
    "value": 10,
    "typeclass": "typeclasses.eatables.Eatable",
    "attrs": [("desc", "A stew designed by Basic Space. It has an odd smell, but promises good health!"),
              ("quality", 'POOR'),
              ("effects", "health")],
}

BS_MULTITOOL = {
    "prototype_key": "BS_MULTITOOL",
    "key": "Multitool",
    "value": 100,
    "typeclasses": "typeclasses.tools.Tools",
    "attrs": [("desc", "A tool designed to handle multiple jobs. Using one increases working efficiency."),
              ("quality", 'POOR')],
}

BS_TABLE = {
    "prototype_key": "BS_TABLE",
    "key": "BS Table",
    "value": 10,
    "typeclasses": "typeclasses.objects.Object",
    "attrs": [("desc", "A simple metal table of poor quality. It looks like it will fall apart soon."),
              ("quality", 'POOR')],
}

BS_CHAIR = {
    "prototype_key": "BS_CHAIR",
    "key": "BS Chair",
    "value": 10,
    "typeclasses": "typeclasses.sitables.Sitable",
    "attrs": [("desc", "A simple metal chair of poor quality. Can it even handle my weight?"),
              ("quality", 'POOR')],
}

BS_BED = {
    "prototype_key": "BS_BED",
    "key": "BS Bed",
    "value": 100,
    "typeclasses": "typeclasses.sitables.Layable",
    "attrs": [("desc", "A simple metal bed made of poor quality. The stuffing looks thin..."),
              ("quality", 'POOR')]
}
##Starter Ships
BS_MINER_ROCKSKIPPER =  {
    "prototype_key": "BS_MINER_ROCKSKIPPER",
    "key": "BS Miner RockSkipper",
    "value": 15000,
    "typeclass": "typeclasses.ships.Miner",
    "attrs": [("desc", "Not the best mining ship, but it is the cheapest. WARNING: Basic Space is not responsible for death/damage caused by asteroids."),
              ("health", 7200),
              ("sheilds", 2500),
              ("max_orehold", 1500),
              ("genhold", 100)],
}
BS_FREIGHTER_SMALLHAULER = {
    "prototype_key": "BS_FREIGHTER_SMALLHAULER",
    "key": "BS Freighter SmallHauler",
    "value": 15000,
    "typeclass": "typeclasses.ships.Freighter",
    "attrs": [("desc", "Basic Space has created a luxurious tank, so you ran rest well knowing the pirates wont even leave a scratch! WARNING: Basic Space is not responsible for any hardship as a result of slow travel."),
               ("health", 5700),
               ("sheilds", 10000),
               ("hold", 10000)]
}
BS_RESEARCHER_ASTEROIDDUST = {
    "prototype_key": "BS_RESEARCHER_ASTEROIDDUST",
    "key": "BS Researcher AsteroidDust",
    "value": 15000,
    "typeclass": "typeclasses.ships.Researcher",
    "attrs": [("desc", "Let Basic Space take you to the corners of the galaxy. WARNING: Basic Space is not responsible for loss of life due to strandenment."),
               ("health", 1000),
               ("sheilds", 5000),
               ("voltilehold", 50),
               ("genhold", 500)]
}
BS_FIGHTER_CRICKET = {
    "prototype_key": "BS_FIGHTER_CRICKET",
    "key": "BS Fighter Cricket",
    "value": 15000,
    "typeclass": "typeclasses.ships.Fighter",
    "attrs": [("desc", "Win battles with Basic Space's skirmisher! WARNING: Not tested against wars."),
               ("health", 3500),
               ("sheilds", 10000),
               ("gunslots", 2),
               ("genhold", 100),
               ("ammohold", 1500)]
}
