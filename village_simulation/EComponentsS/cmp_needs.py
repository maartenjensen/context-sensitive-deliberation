
class CmpNeeds:

    def __init__(self):

        self.hunger = 0
        self.sleep = 0
        self.work = 0
        self.socialize = 0

    def get_str(self):

        return "Hun: " + str(self.hunger) + ", Sle: " + str(self.sleep) + ", Work: " + str(self.work)