# in evadventure/tests/test_combat.py 

from unittest.mock import Mock, patch
from evennia.utils.test_resources import EvenniaCommandTestMixin

from world.combat_twitch import CombatTwitchHandler

# ...

class TestEvAdventureTwitchCombat(EvenniaCommandTestMixin):

    def setUp(self): 
        self.combathandler = (
                combat_twitch.EvAdventureCombatTwitchHandler.get_or_create_combathandler(
            self.char1, key="combathandler") 
        )
   
    @patch("evadventure.combat_twitch.unrepeat", new=Mock())
    @patch("evadventure.combat_twitch.repeat", new=Mock())
    def test_hold_command(self): 
        self.call(combat_twitch, CmdHold(), "", "You hold back, doing nothing")
        self.assertEqual(self.combathandler.action_dict, {"key": "hold"})
            