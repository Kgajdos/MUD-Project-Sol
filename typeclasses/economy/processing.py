from evennia import DefaultScript
from evennia.prototypes.spawner import spawn
from .recipes import GOOD_PROCESSING_RECIPES

class ProcessingStation:
    """
    Periodically processes goods based on the station type
    """

    def at_script_creation(self):
        self.key = "processing_script"
        self.desc = "Processes goods in the background"
        self.interval = 60
        self.persistent = True
        self.db.station_type = None
        self.db.processing_queue = []
        self.db.processed_log = {}

    def add_to_queue(self, good, processing_time):
        self.db.processing_queue.append([good, processing_time])

    def at_repeat(self):
        """
        Called every tick (hooked to a script or a handler).
        Decreases processing time and completes jobs.
        """
        new_queue = []
        for good, time_left in self.db.processing_queue:
            time_left -= 1
            if time_left <= 0:
                self.complete_processing(good)
            else:
                new_queue.append([good, time_left])
        self.db.processing_queue = new_queue

    def complete_processing(self, good):
        recipes = GOOD_PROCESSING_RECIPES.get(good.key, [])
        log = self.db.processed_log or {}
        for recipe in recipes:
            if recipe.get("station") != self.station_type:
                continue

            #Handle main output
            for _ in range(recipe.get("output_qty", 1)):
                spawn(recipe["prototype"], location=self.location)

            #handle byproducts if defined
            for byproduct in recipe.get("byproduct", []):
                qty = byproduct.get("qty", 1)
                proto = byproduct["prototype"]
                for _ in range(qty):
                    spawn(proto, location=self.location)

                key = proto.get("key", "byproduct")
                log[key] = log.get(key, 0) + qty
            
            good.delete()

            #Creates a log for that specific station
            key = recipe.get("output", "Unknown")
            log[key] = log.get(key, 0) + recipe.get("output_qty", 1)
            self.db.processed_log = log
            break


class Refinery(ProcessingStation):
    def __init__(self):
        self.db.station_type = "refinery"

class Forge(ProcessingStation):
    def at_script_creation(self):
        self.db.station_type = "forge"

class Fabricator(ProcessingStation):
    def at_script_creation(self):
        self.db.station_type = "fabricator"

class Packager(ProcessingStation):
    def at_script_creation(self):
        self.db.station_type = "packager"