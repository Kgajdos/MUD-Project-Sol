"""
Player class helpers — these wrap a Character and store progression data on
`character.db` so values are persistent across reloads. They provide a small
API for adding experience and leveling up.
"""

class BasePlayerClass:
    """Base wrapper that stores state under `character.db['playerclass_<key>']`.

    Data layout stored on the character is a simple dict:
        {"level": int, "xp": int, "xp_required": int}
    """

    key = "base"

    def __init__(self, character):
        self.character = character
        self._dbkey = f"playerclass_{self.key}"
        if not isinstance(self.character.db.get(self._dbkey), dict):
            # initialize defaults
            self.character.db[self._dbkey] = {
                "level": 1,
                "xp": 0,
                "xp_required": 100,
            }

    @property
    def data(self):
        return self.character.db.get(self._dbkey, {})

    @property
    def level(self):
        return int(self.data.get("level", 1))

    @property
    def xp(self):
        return int(self.data.get("xp", 0))

    @property
    def xp_required(self):
        return int(self.data.get("xp_required", 100))

    def _save_data(self, data):
        self.character.db[self._dbkey] = data

    def add_xp(self, amount):
        """Add experience; handle level ups. Returns number of levels gained."""
        if amount <= 0:
            return 0
        data = dict(self.data) or {"level": 1, "xp": 0, "xp_required": 100}
        data["xp"] = data.get("xp", 0) + int(amount)
        levels_gained = 0
        # level up while we have enough XP
        while data["xp"] >= data["xp_required"]:
            data["xp"] -= data["xp_required"]
            data["level"] = data.get("level", 1) + 1
            # simple scaling for required XP; tweak multiplier as desired
            data["xp_required"] = int(data["xp_required"] * 1.25)
            levels_gained += 1
        self._save_data(data)
        return levels_gained

    def to_dict(self):
        return dict(self.data)


class Miner(BasePlayerClass):
    key = "miner"


class Freighter(BasePlayerClass):
    key = "freighter"


class Researcher(BasePlayerClass):
    key = "researcher"


class Fighter(BasePlayerClass):
    key = "fighter"


# Convenience factory if other code expects to call these with a character
# e.g. `playerclass.Miner(character)` still works and returns a helper.


__all__ = ["BasePlayerClass", "Miner", "Freighter", "Researcher", "Fighter"]


