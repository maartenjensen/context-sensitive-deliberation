import mesa

from village_simulation.Agent.agent_schedules import ScheduleTime
from village_simulation.Agent.agent_systems import AgentFood, AgentEconomy, AgentPosition
from village_simulation.Building.buildings import House


class HumanParent(mesa.Agent):

    def __init__(self, unique_id, model, pos, my_house: House):
        super().__init__(unique_id, model)

        # Agent systems
        self.position = AgentPosition(unique_id, pos, my_house)
        self.food = AgentFood()
        self.economy = AgentEconomy()

        # Deliberation and context
        self.schedule_time = ScheduleTime()


class Human(HumanParent):
    """ An agent with some money """

    def __init__(self, unique_id, model, pos, my_house: House):
        super().__init__(unique_id, model, pos, my_house)

        # Agent systems
        self.position = AgentPosition(unique_id, pos, my_house)
        self.food = AgentFood()
        self.economy = AgentEconomy()

        # Deliberation and context
        self.schedule_time = ScheduleTime()

        # Initialisation functions
        self.model.schedule.add(self)
        self.schedule_time.init_schedule_default_worker(self.food.default_food)

        self.position.move_to_house()

    def step(self):
        # Input context sensitive deliberation
        print("#####################################")

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", "
        info += "Money: " + str(self.economy.money) + " (" + str(self.economy.salary) + ")"
        if self.position.has_bike:
            info += ", Car"
        if self.position.has_bike:
            info += ", Bike"
        info += ", B:" + str(self.food.beef) + ",C:" + str(self.food.chicken) + ",T:" + str(self.food.tofu)
        return info
