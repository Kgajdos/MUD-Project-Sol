import evennia
from evennia import DefaultObject
from evennia import create_object, search_object
from typeclasses.asteroids import Asteroid

resource_quantities = {
    "Nickle": 30,
    "Silver": 15,
    "Gold": 5,
    "Silicate": 1
}

asteroid = Asteroid.generate_asteroid(resource_quantities)
asteroid.generate_asteroid(resource_quantities)
contents = asteroid.display_resource_contents()

print(contents)



