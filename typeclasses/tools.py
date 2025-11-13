from typeclasses.objects import Object

# Class that defines tools and how they interact with the world
class Tools(Object):

    def at_object_creation(self):
        super().at_object_creation()
        # store simple, serializable attributes on the db
        self.db.toolquality = "poor"
        self.db.modifier = 0.0

    def set_tool_quality(self, percentage):
        """Set tool quality based on a percentage (0.0-1.0).
        Also stores a numeric modifier suitable for calculations.
        """
        try:
            percentage = float(percentage)
        except Exception:
            percentage = 0.0
        self.db.modifier = percentage
        if percentage < 0.05:
            self.db.toolquality = "Poor"
        elif percentage < 0.10:
            self.db.toolquality = "Low"
        elif percentage < 0.15:
            self.db.toolquality = "Medium"
        elif percentage < 0.20:
            self.db.toolquality = "Good"
        elif percentage < 0.25:
            self.db.toolquality = "Great"
        else:
            self.db.toolquality = "Extraordinary"

    @staticmethod
    def tool_advantage(tool, base_value):
        """Return the modified value based on the tool's modifier.
        tool may be an object instance or a dict-like with a 'modifier'.
        """
        modifier = 0.0
        if hasattr(tool, 'db'):
            modifier = getattr(tool.db, 'modifier', 0.0) or 0.0
        elif isinstance(tool, dict):
            modifier = tool.get('modifier', 0.0) or 0.0
        try:
            return base_value + base_value * float(modifier)
        except Exception:
            return base_value
