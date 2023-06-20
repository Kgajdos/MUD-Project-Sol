from typeclasses.objects import Object


#Class that defines tools and how they interact with the world
class Tools(Object):

    def at_object_creation(self):
        pass

    #The idea here is that tools will give a % extra based on tool quality (Poor = 1, Low = 5%, Med = 10%, Good = 15%, Great = 20%, Extrodinary = 25%) 
    #self.db.quality is a number to represent a %, the noun will be represented in its description and not handled here!
    def tool_advantage(self, caller):
        tool_quality = self.ToolQuality
        return caller * tool_quality
