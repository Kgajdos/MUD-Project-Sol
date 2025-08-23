import yaml
from evennia import create_object, search_object
from typeclasses.rooms import Room
from typeclasses.exits import Exit
from typeclasses.npc import NPC

class StationLoader:
    def __init__(self, yaml_path):
        with open(yaml_path, "r") as f:
            self.data = yaml.safe_load(f)
        self.room_map = {}

    def load(self):
        self._load_station()
        self._load_rooms()
        self._load_npcs()

    def _load_station(self):
        name = self.data.get("name")
        location = self.data.get("location")


    def _load_rooms(self):
        # First pass: create all rooms
        for room_data in self.data.get("rooms", []):
            self._create_room(room_data)

        # Second pass: create all exits
        for room_data in self.data.get("rooms", []):
            room = self.room_map[str(room_data["id"])]
            self._create_exits(room, room_data.get("exits", []))


    def _create_room(self, data):
        room_id = str(data["id"]).lower()  # Internal ID
        existing = [r for r in search_object(data["name"]) if r.db.room_id == room_id]
        if existing:
            room = existing[0]
        else:
            room = create_object(Room, key=data["name"])  # Visible room name
            room.db.room_id = room_id
            room.db.desc = data["description"]
        self.room_map[room_id] = room
        return room



    def _create_exits(self, origin, exits):
        for exit_data in exits:
            to_id = str(exit_data["to"]).lower()
            destination = self.room_map.get(to_id)
            if not destination:
                print(f"  ⚠️  Destination not found for ID {to_id}")
                continue
            if not any(e.key.lower() == exit_data["direction"].lower() for e in origin.exits):
                create_object(Exit, key=exit_data["direction"], location=origin, destination=destination)
                print(f"  ✅ Exit '{exit_data['direction']}' created from '{origin.key}' to '{destination.key}'")


    def _load_npcs(self):
        for npc_data in self.data.get("npcs", []):
            location = self.room_map.get(npc_data["location"])
            if not location:
                continue
            existing = [n for n in search_object(npc_data["name"]) if n.location == location]
            if existing:
                continue  # Avoid duplicates
            npc = create_object(NPC, key=npc_data["name"], location=location)
            npc.db.traits = npc_data.get("traits", {})
            npc.db.desc = npc_data.get("description", "")
            npc.db.dialog = npc_data.get("dialog")
            npc.db.role = npc_data.get("role")