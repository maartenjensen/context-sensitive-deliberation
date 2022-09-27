from village_simulation.Agent.Data.enums import DefaultFood
from village_simulation.Common.sim_utils import SimUtils


class AgentFood:

    def __init__(self):

        self.beef = SimUtils.get_model().random.randint(0, 5)
        self.chicken = SimUtils.get_model().random.randint(0, 5)
        self.tofu = SimUtils.get_model().random.randint(0, 5)

        # Default food
        self.default_food = DefaultFood.BEEF
        if self.chicken > self.beef:
            self.default_food = DefaultFood.CHICKEN
        if self.tofu > self.chicken and self.tofu > self.beef:
            self.default_food = DefaultFood.TOFU

        # Utility
        self.ut_beef = self.beef
        self.ut_chicken = self.chicken
        self.ut_tofu = self.tofu

    def get_total_food(self):
        return self.beef + self.chicken + self.tofu
