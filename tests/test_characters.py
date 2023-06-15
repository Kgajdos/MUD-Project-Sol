from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest

from typeclasses.characters import Character

class TestCharacters(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        self.character = create.create_object(Character, key = "TestChar")

    def test_heal(self):
        self.character.hp = 0
        self.character.hp_max = 8

        self.character.heal(1) #<----This is accessing health, which is in cat(1)
        self.assertEqual(self.character.hp, 1)
        #Make sure we cant over heal
        self.character.heal(100)
        self.assertEqual(self.character.hp, 8)

    def test_at_pay(self):
        self.character.coins = 100

        result = self.character.at_pay(60)
        self.assertEqual(result, 60)
        self.assertEqual(self.character.coins, 40)

        #Testing that we cant get more coins than we have
        result = self.character.at_pay(100)
        self.assertEqual(result, 40)
        self.assertEqual(self.character.coins, 0)