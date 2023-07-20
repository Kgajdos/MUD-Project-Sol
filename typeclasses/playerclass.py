class Miner():
    def __init__(self, character):
        # Initialize the Miner class attributes and functionality
        character.mining_level = 1
        character.mining_experience = 0
        character.mining_experience_required = 100


class Freighter():
    def __init__(self, character):
        character.hauling_level = 1
        character.hauling_experience = 0
        character.hauling_experience_required = 100


class Researcher():
    def __init__(self, character):
        character.research_level = 1
        character.research_experience = 0
        character.research_experience_required = 100

class Fighter():
    def __init__(self, character):
        character.fighting_level = 1
        character.fighting_experience = 0
        character.fighting_experience_required = 100


