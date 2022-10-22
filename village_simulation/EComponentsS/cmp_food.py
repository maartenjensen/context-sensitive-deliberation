from village_simulation.EComponentsS.enums import DefaultFood
from village_simulation.Common.sim_utils import SimUtils


class CmpFood:

    def __init__(self):

        self.beef = 0
        self.chicken = 0
        self.tofu = 0
        if SimUtils.get_model().random.random() < 0.334:
            self.beef = 3
        elif SimUtils.get_model().random.random() < 0.5:
            self.chicken = 3
        else:
            self.tofu = 3

        # Temporary chicken
        self.beef = 3
        self.chicken = 3
        self.tofu = 3


        # Default food
        self.default_food = DefaultFood.BEEF
        if self.chicken > self.beef:
            self.default_food = DefaultFood.CHICKEN
        if self.tofu > self.chicken and self.tofu > self.beef:
            self.default_food = DefaultFood.TOFU

        self.buy_food_amount = 3

        # Utility
        self.ut_beef = self.beef
        self.ut_chicken = self.chicken
        self.ut_tofu = self.tofu

    def get_total_food(self):
        return self.beef + self.chicken + self.tofu
