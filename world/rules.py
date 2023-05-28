from random import randint

def roll_hit():
    """Roll 1d100"""
    return randint(1,100)

def roll_dmg():
    """Roll 1d6"""
    return randint(1,6)

def check_defeat(character):
    """Checks if the character is defeated"""
    #character.db.HP is current health, character.db.stats["health"] is max health
    if character.db.HP <= 0:
        character.msg("You pass out.")
        character.db.HP = character.db.stats['Health']

def add_XP(character, skill, amount):
    """Add XP to the character to track leveling."""
    character.db.skill['exp'] += amount
    if character.db.skill['exp'] >= (character.db.skill['level'] +1) ** 2:
        character.db.skill['level'] += 1
        character.db.skill['exp'] = 0
        character.msg(f"You've leveled {skill} to level {character.db.skill['level']}!")

def calc_combatpower(character):
    """
    This function calculates a character's combatpower modifier. This does not replace a roll, it only adds to the value.

    There is no need to specify if attacking or defending.
    """
    physical = character.db.stats["Physical"] / 2
    mental = character.db.stats["Mental"] / 2
    #TODO: Implement a weapons system
    #TODO: Other bonuses would go here.
    return physical + mental
