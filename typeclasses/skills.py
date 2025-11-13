"""
Skill utilities for the project.

This module contains helpers for creating and managing skill entries that are
stored on a Character's `.db` mapping. It also provides an authoritative,
YAML-backed skill registry so UI and game logic can consistently query which
skills exist and what their defaults are.
"""
from pathlib import Path
from typing import Dict

# Try to import PyYAML, but fall back gracefully if it's not installed.
try:
    import yaml
except Exception:
    yaml = None

# Default path for the skills YAML file (project-root/data/skills.yml)
_SKILL_FILE = Path(__file__).resolve().parent.parent / "data" / "skills.yml"

# A small in-code default registry used if there is no YAML file.
_default_registry: Dict[str, Dict] = {
    "cooking": {"label": "Cooking", "selectable": True, "category": "life", "xp_required": 100, "description": "Preparing food."},
    "diplomacy": {"label": "Diplomacy", "selectable": True, "category": "social", "xp_required": 120, "description": "Negotiation and persuasion."},
    "fabricating": {"label": "Fabricating", "selectable": True, "category": "trade", "xp_required": 110, "description": "Building components."},
    "guns": {"label": "Firearms", "selectable": True, "category": "combat", "xp_required": 140, "description": "Ranged weapons and maintenance."},
    "logic": {"label": "Logic", "selectable": True, "category": "mental", "xp_required": 100, "description": "Reasoning and puzzles."},
    "luck": {"label": "Luck", "selectable": True, "category": "misc", "xp_required": 100, "description": "Fortune and chance."},
    "mechanic": {"label": "Mechanic", "selectable": True, "category": "trade", "xp_required": 110, "description": "Repair and maintenance."},
    "melee": {"label": "Melee", "selectable": True, "category": "combat", "xp_required": 120, "description": "Close-quarters combat."},
    "piloting": {"label": "Piloting", "selectable": True, "category": "skill", "xp_required": 130, "description": "Ship piloting."},
    "tinkering": {"label": "Tinkering", "selectable": True, "category": "trade", "xp_required": 105, "description": "Small inventions and tweaks."},
    "trade": {"label": "Trade", "selectable": True, "category": "economy", "xp_required": 100, "description": "Barter and commerce."},
}

# In-memory registry used by the game. Loaded from YAML if available.
AVAILABLE_SKILLS: Dict[str, Dict] = {}


def load_skill_registry(path: Path = None) -> Dict[str, Dict]:
    """Load a skill registry from YAML file. If YAML is unavailable or file
    missing, fall back to the in-code default registry.
    """
    global AVAILABLE_SKILLS
    path = Path(path) if path else _SKILL_FILE
    if path.exists() and yaml is not None:
        try:
            with open(path, "r", encoding="utf8") as fh:
                data = yaml.safe_load(fh) or {}
                # Ensure keys are strings and values are dicts
                data = {str(k): dict(v or {}) for k, v in data.items()}
                AVAILABLE_SKILLS = data
                return AVAILABLE_SKILLS
        except Exception:
            # On any error, fall back to defaults
            pass

    # fallback
    AVAILABLE_SKILLS = dict(_default_registry)
    return AVAILABLE_SKILLS


# Load at import time
load_skill_registry()


def reload_skill_registry(path: Path = None) -> Dict[str, Dict]:
    """Force reloading the registry from disk and return it."""
    return load_skill_registry(path)


def save_skill_registry(path: Path = None) -> bool:
    """Write the current in-memory registry back to YAML. Returns True on
    success. If PyYAML is not available this will return False.
    """
    if yaml is None:
        return False
    path = Path(path) if path else _SKILL_FILE
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf8") as fh:
            yaml.safe_dump(AVAILABLE_SKILLS, fh, sort_keys=True)
        return True
    except Exception:
        return False


def get_skill_meta(skill_key: str) -> Dict:
    return AVAILABLE_SKILLS.get(skill_key, {})


def get_all_skill_keys() -> list:
    return list(AVAILABLE_SKILLS.keys())


def get_selectable_skill_keys() -> list:
    return [k for k, v in AVAILABLE_SKILLS.items() if v.get("selectable", True)]


def get_default_xp_required(skill_key: str, fallback: int = 100) -> int:
    return int(get_skill_meta(skill_key).get("xp_required", fallback))


def register_skill(skill_key: str, meta: Dict, write_back: bool = False) -> None:
    """Register or update a skill in the in-memory registry. If write_back
    is True, attempt to save the YAML file as well.
    """
    AVAILABLE_SKILLS[str(skill_key)] = dict(meta or {})
    if write_back:
        save_skill_registry()


# backwards-compatible helpers previously present in this module
def make_skill_entry(level=1, xp=0, xp_required=100):
    return {"level": int(level), "xp": int(xp), "xp_required": int(xp_required)}

_make_skill_entry = make_skill_entry


def init_skills_on_char(char, selected_skills):
    skills = {name: make_skill_entry(xp_required=get_default_xp_required(name)) for name in selected_skills}
    char.db.skills = skills
    return skills


def add_skill_xp(char, skill_name, amount):
    if amount <= 0:
        return 0
    skills = getattr(char.db, "skills", {}) or {}
    if skill_name not in skills:
        skills[skill_name] = make_skill_entry(xp_required=get_default_xp_required(skill_name))
    entry = skills[skill_name]
    entry["xp"] = int(entry.get("xp", 0)) + int(amount)
    levels_gained = 0
    while entry["xp"] >= entry["xp_required"]:
        entry["xp"] -= entry["xp_required"]
        entry["level"] = int(entry.get("level", 1)) + 1
        entry["xp_required"] = int(entry.get("xp_required", 100) * 1.25)
        levels_gained += 1
    char.db.skills = skills
    return levels_gained


def format_skill_display(name, entry):
    return f"{name} (Lv {entry.get('level',1)} {entry.get('xp',0)}/{entry.get('xp_required',100)})"


__all__ = [
    "AVAILABLE_SKILLS",
    "load_skill_registry",
    "reload_skill_registry",
    "save_skill_registry",
    "get_skill_meta",
    "get_all_skill_keys",
    "get_selectable_skill_keys",
    "get_default_xp_required",
    "register_skill",
    "make_skill_entry",
    "_make_skill_entry",
    "init_skills_on_char",
    "add_skill_xp",
    "format_skill_display",
]
