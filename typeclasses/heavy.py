from evennia.objects.objects import DefaultObjects

class Heavy(DefaultObjects):
    
    def at_object_creation(self):
        #lock the object down by default
        self.locks.add("get:false()")
           # the default "get" command looks for this Attribute in order
           # to return a customized error message (we just happen to know
           # this, you'd have to look at the code of the 'get' command to
           # find out).
        self.db.get_err_msg = "This is too heavy to pick up."

    def return_appearance(self):
        