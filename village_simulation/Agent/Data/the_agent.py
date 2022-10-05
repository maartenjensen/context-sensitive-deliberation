import mesa

from village_simulation.Agent.Data.data_car import AgentDataCar
from village_simulation.Agent.Data.data_deliberation import AgentDataDeliberation
from village_simulation.Agent.Data.data_economy import AgentEconomy
from village_simulation.Agent.Data.data_food import AgentFood
from village_simulation.Agent.Data.data_needs import AgentDataNeeds
from village_simulation.Agent.Data.data_position import AgentPosition
from village_simulation.Agent.Data.data_social_groups import AgentDataSocialGroups
from village_simulation.Agent.Data.data_time_schedule import TimeSchedule
from village_simulation.Agent.Data.data_values import AgentDataValues


class HumanParent(mesa.Agent):

    def __init__(self, unique_id, model, pos, my_house_id, my_shop_id, my_office_id):
        super().__init__(unique_id, model)

        # Agent systems
        self.position = AgentPosition(unique_id, pos, my_house_id, my_shop_id, my_office_id)
        self.food = AgentFood()
        self.economy = AgentEconomy()
        self.car = AgentDataCar()
        self.deliberation = AgentDataDeliberation()
        self.data_social_groups = AgentDataSocialGroups()
        self.values = AgentDataValues()
        self.needs = AgentDataNeeds()

        # Deliberation and context
        self.schedule_time = TimeSchedule()


class Human(HumanParent):
    """ An agent with some money """

    def __init__(self, unique_id, model, pos, my_house_id, my_shop_id, my_office_id):
        super().__init__(unique_id, model, pos, my_house_id, my_shop_id, my_office_id)

        # Agent systems
        self.position = AgentPosition(unique_id, pos, my_house_id, my_shop_id, my_office_id)
        self.food = AgentFood()
        self.economy = AgentEconomy()
        self.deliberation = AgentDataDeliberation()
        self.data_social_groups = AgentDataSocialGroups()

        # Deliberation and context
        self.schedule_time = TimeSchedule()

        # Initialisation functions
        self.model.schedule.add(self)

    def step(self):
        # Input context sensitive deliberation, I want the deliberator to take control over the behavior of the agent
        # this works better in python because of problems with cyclic imports, so I made a separation between data
        # and the manipulating systems
        print("#####################################")

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", "
        info += "Money: " + str(self.economy.money) + " (" + str(self.economy.salary) + ")"
        if self.position.has_bike:
            info += ", Car"
        if self.position.has_bike:
            info += ", Bike"
        info += ", B:" + str(self.food.beef) + ",C:" + str(self.food.chicken) + ",T:" + str(self.food.tofu)
        info += ", Social group: " + str(self.data_social_groups.my_group)
        return info
