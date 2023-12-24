from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest

from typeclasses.drinkables import Drinkables

class TestDrinkables(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        self.drink = create.create_object(Drinkables, "Cup of Water", None)

    def test_drink(self):
        print(self.drink.name)
