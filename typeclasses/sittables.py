from evennia import DefaultObject
from commands.sittables import CmdSetSit

class Sittable(DefaultObject):

    #def at_object_creation(self):
    #    self.cmdset.add_default(CmdSetSit)

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.

        Args:
            sitter (Object): The one trying to sit down.
        """
        adjective = self.db.adjective or "on"
        current = self.db.sitter
        if current:
            if current == sitter:
                sitter.msg(f"You are already sitting {adjective} {self.key}.")
            else:
                sitter.msg(f"You can't sit {adjective} {self.key} "
                           f"- {current.key} is already sitting there!")
                
            return
        self.db.sitter = sitter
        sitter.db.is_sitting = self
        sitter.msg(f"You sit {adjective} {self.key}.")

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.
        """
        current = self.db.sitter
        if not stander == current:
            stander.msg(f"You are not sitting {self.db.adjective} {self.key}.")
        else:
            self.db.sitter = None
            del stander.db.is_sitting
            stander.msg(f"You stand up from {self.key}.")

class Layables(Sittable):
        
        def do_lay(self, player):
            """
            Called when trying to lay on this object.

            Args:
                player (Object): The one trying to lay down.
            """
            adjective = self.db.adjective or "on"
            current = self.db.player
            if current:
                if current == player:
                    player.msg(f"You are already laying {adjective} {self.key}.")
                else:
                    player.msg(f"You can't lay {adjective} {self.key} "
                            f"- {current.key} is already laying there!")
                return
            self.db.player = player
            player.db.is_sitting = self
            player.msg(f"You lay {adjective} {self.key}.")

        def do_stand(self, stander):
            """
            Called when trying to stand from this object.

            Args:
                stander (Object): The one trying to stand up.
            """
            current = self.db.player
            if not stander == current:
                stander.msg(f"You are not laying {self.db.adjective} {self.key}.")
            else:
                self.db.player = None
                del stander.db.is_sitting
                stander.msg(f"You stand up from {self.key}.")