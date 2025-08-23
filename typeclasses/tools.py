from typeclasses.objects import Object
from evennia import AttributeProperty

#Class that defines tools and how they interact with the world
class Tools(Object):

    def at_object_creation(self):
        self.ToolQuality = AttributeProperty.attributes.add("toolquality", "poor")
        self.modifier = AttributeProperty.attributes.add("modifier", None)
        self.set_tool_quality


    #The idea here is that tools will give a % extra based on tool quality (Poor = 0%, Low = 5%, Med = 10%, Good = 15%, Great = 20%, Extrodinary = 25%) 
    #self.ToolQuality is a number to represent a %
    @staticmethod
    def set_tool_quality(self, percentage):
        self.modifier = percentage
        if percentage < .05:
            self.ToolQuality = "Poor"
        elif percentage > .05 and percentage < .1:
            self.ToolQuality = "Low"
        elif percentage > .1 and percentage < .15:
            self.ToolQuality = "Medium"
        elif percentage > .15 and percentage < .2:
            self.ToolQuality = "Good"
        elif percentage > .2 and percentage < .25:
            self.ToolQuality = "Great"
        elif percentage > .25:
            self.ToolQuality = "Extrodinary"
        else:
            self.ToolQuality = "Broken"

    @classmethod
    def tool_advantage(cls, self, caller):
        tool_quality = self.ToolQuality
        return caller * tool_quality
