import mesa
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

        # Enums
        self.activity = Activity.RELAXING
        self.plan = Plan.NONE
        self.need = Need.NONE
        self.goal = Goal.NONE