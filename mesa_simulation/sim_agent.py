import mesa
from csd_framework.csd_deliberator import Deliberator

class MyAgent(mesa.Agent):
    """An agent with some money"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.money = 50
        self.food = 20
        # Input model of context
        self.myDeliberator = Deliberator()

    def action_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        # Input context sensitive deliberation
        print("#####################################")
        print("Agent " + str(self.unique_id) + " deliberates")
        self.myDeliberator.main_deliberate()
        print("#####################################")

class MyLocation(mesa.Agent):
    """Buildings"""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        print("Added a building")

    def step(self):
        print("A building exists")

