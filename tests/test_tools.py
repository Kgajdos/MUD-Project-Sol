from evennia.utils import create
from evennia.utils.test_resources import BaseEvenniaTest

from typeclasses.tools import Tools

class TestTools(BaseEvenniaTest):
    def setUp(self):
        super().setUp()
        self.tool = create.create_object(Tools, "Tattered MultiTool", None)

    def test_tool(self):
        print(self.tool.name)
