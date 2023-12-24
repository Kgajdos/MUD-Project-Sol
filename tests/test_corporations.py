from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest

from typeclasses.corporations import Corporation

class TestCorporations(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        self.corporation = create.create_object(Corporation, key = "TestCorp")
        self.employee = create.create_object(typeclass = "typeclasses.characters.Character", key = "Bob")

    def test_hire_employee(self):
        self.corporation.hire_employee(self.employee, "Fighter")

    def test_pay_employee(self):
        self.corporation.pay_employee(self.employee, 1000)

    def test_fire_employee(self):
        self.corporation.fire_employee(self.employee)

    def test_show_employees(self):
        self.corporation.show_employees()

    def test_add_to_reserves(self):
        temp_dict = {"iron": 20, "copper": 100}
        self.corporation.add_to_reserves(temp_dict)

    def test_display_reserves(self):
        self.corporation.display_reserves()

    def test_create_cargo_crate(self):
        resources = {"iron": 1000}
        cargo = create.create_object(typeclass = "typeclasses.objects.Object", key = "Ammo")
        self.crate = self.corporation.create_cargo_crate(resources, cargo)