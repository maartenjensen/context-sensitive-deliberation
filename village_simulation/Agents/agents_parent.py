import mesa

from new_csd_framework.csd_context_ontology import DefaultFood
from village_simulation.Agents.enums import Activity, Plan, Need, Goal


class ParentAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Variables
        self.model = model
        self.pos = (0, 0)
        self.my_house = None
        self.location = None
        self.has_bike = False
        self.has_car = False
        self.money = 0
        self.beef = 0
        self.chicken = 0
        self.tofu = 0
        self.actions = None

        # Enums
        self.activity = Activity.RELAXING
        self.plan = Plan.NONE
        self.need = Need.NONE
        self.goal = Goal.NONE

        # Default food
        self.default_food = DefaultFood.NONE

        # Utility
        self.ut_beef = self.beef
        self.ut_chicken = self.chicken
        self.ut_tofu = self.tofu
