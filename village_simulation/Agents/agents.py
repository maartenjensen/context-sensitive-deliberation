from enum import Enum

import mesa

from csd_framework.csd_context_explorer import ContextExplorer
from csd_framework.csd_deliberator import Deliberator
from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Agents.buildings import House
from village_simulation.Agents.enums import Activity, Plan, Need, Goal
from village_simulation.Model.model_parent import MesaParentModel


class MyAgent(ParentAgent):
    """An agent with some money"""

    def __init__(self, unique_id, model: MesaParentModel, pos, my_house: House):
        super().__init__(unique_id, model)
        # Variables
        self.model = model
        self.pos = pos
        self.my_house = my_house
        self.location = None
        self.has_bike = self.model.random.getrandbits(1)
        self.has_car = self.model.random.getrandbits(1)
        self.money = 50
        self.beef = 0
        self.chicken = 0
        self.tofu = 0

        # Enums
        self.activity = Activity.RELAXING
        self.plan = Plan.NONE
        self.need = Need.NONE
        self.goal = Goal.NONE

        # Complex variables
        self.my_deliberator = Deliberator()
        self.context_explorer = ContextExplorer()

        # Functions
        self.model.schedule.add(self)
        self.move_to_house()

    def action_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        # Input context sensitive deliberation
        print("#####################################")
        print("Agent " + str(self.unique_id) + " retrieves context")
        print(self.context_explorer.get_primary_information(self))
        # self.my_deliberator.main_deliberate()
        print("#####################################")

    def move_to_house(self):
        self.pos = self.my_house.get_random_position_on()
        self.model.grid.place_agent(self, self.pos)
        self.location = self.my_house

    def get_food(self):
        return self.beef + self.chicken + self.tofu

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", "
        info += "Money: " + str(self.money)
        if self.has_car:
            info += ", Car"
        if self.has_bike:
            info += ", Bike"
        info += ", B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        return info
