from village_simulation.Agent.enums import DefaultFood
from village_simulation.Building.buildings import House
from village_simulation.Model.sim_utils import SimUtils


class AgentPosition:

    def __init__(self, unique_id, pos, my_house: House):

        self.unique_id = unique_id
        self.pos = pos
        self.my_house = my_house
        self.location = None
        self.has_bike = SimUtils.get_model().random.getrandbits(1)
        self.has_car = SimUtils.get_model().random.getrandbits(1)

    def action_move(self):
        possible_steps = SimUtils.get_model().grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = SimUtils.get_model().random.choice(possible_steps)
        SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(self.unique_id), new_position)

    def move_to_house(self):
        self.pos = self.my_house.get_random_position_on()
        SimUtils.get_model().grid.place_agent(SimUtils.get_agent_by_id(self.unique_id), self.pos)
        self.location = self.my_house


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

    def get_food(self):
        return self.beef + self.chicken + self.tofu


class AgentEconomy:

    def __init__(self):

        self.money = 50
        self.salary = 500
