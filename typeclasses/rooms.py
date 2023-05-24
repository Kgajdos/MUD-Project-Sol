"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    @property
    def x(self):
        """Return the X coordinate or None."""
        x = self.tags.get(category="coordx")
        return int(x) if isinstance(x, str) else None
    
    @x.setter
    def x(self, x):
        """Change the X coordinate"""
        old = self.tags.get(category="coordx")
        if old is not None:
            self.tags.remove(old, category="coordx")
        if x is not None:
            self.tags.add(str(x), category="coordx")

    @property
    def y(self):
        """Return the Y coordinate or None."""
        y = self.tags.get(category="coordy")
        return int(y) if isinstance(y, str) else None
    @y.setter
    def y(self, y):
        """Change the Y coordinate."""
        old = self.tags.get(category="coordy")
        if old is not None:
            self.tags.remove(old, category="coordy")
        if y is not None:
            self.tags.add(str(y), category="coordy")

    @property
    def z(self):
        """Return the Z coordinate or None."""
        z = self.tags.get(category="coordz")
        return int(z) if isinstance(z, str) else None
    @z.setter
    def z(self, z):
        """Change the Z coordinate"""
        old = self.tags.get(category="coordz")
        if old is not None:
            self.tags.remove(old, category="coordz")
        if z is not None:
            self.tags.add(str(z), category="coordz")

            
    pass

