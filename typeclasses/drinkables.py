from evennia import create_object
class Drinkables:
    #effects must come in as a dict with a name, an attribute it effects, and effect multiplier
    def makedrinkable(name, desc, effects):
        drink = create_object("typeclasses.drinkables.Drinkable", name = name, desc = desc)
        drink.db.effects = effects
        return drink
