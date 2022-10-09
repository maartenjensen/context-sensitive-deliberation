
class CmpNeeds:

    def __init__(self):

        self.sleep = 0
        self.work = 0
        self.socialize = 0
        self.hunger = 0
        self.food_safety = 0

    def get_str(self):

        return ", Sle:" + "{:.2f}".format(self.sleep) + ", Work:" + "{:.2f}".format(self.work) \
                + "Hun:" + "{:.2f}".format(self.hunger) + ", Food:" + "{:.2f}".format(self.food_safety) \
                + ", Soc:" + "{:.2f}".format(self.socialize)
