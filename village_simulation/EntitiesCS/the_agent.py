import mesa

from village_simulation.EComponentsS.cmp_car import CmpCar
from village_simulation.EComponentsS.cmp_deliberation import CmpDeliberation
from village_simulation.EComponentsS.cmp_economy import CmpEconomy
from village_simulation.EComponentsS.cmp_food import CmpFood
from village_simulation.EComponentsS.cmp_needs import CmpNeeds
from village_simulation.EComponentsS.cmp_position import CmpPosition
from village_simulation.EComponentsS.cmp_social_groups import CmpSocialGroups
from village_simulation.EComponentsS.cmp_time_schedule import CmpTimeSchedule
from village_simulation.EComponentsS.cmp_values import CmpValues


class HumanParent(mesa.Agent):

    def __init__(self, unique_id, model, pos, my_house_id, my_shop_id, my_office_id):
        super().__init__(unique_id, model)

        # Agent systems
        self.position = CmpPosition(unique_id, pos, my_house_id, my_shop_id, my_office_id)
        self.food = CmpFood()
        self.economy = CmpEconomy()
        self.car = CmpCar()
        self.deliberation = CmpDeliberation()
        self.data_social_groups = CmpSocialGroups()
        self.values = CmpValues()
        self.needs = CmpNeeds()

        # Deliberation and context
        self.schedule_time = CmpTimeSchedule()


class Human(HumanParent):
    """ An agent with some money """

    def __init__(self, unique_id, model, pos, my_house_id, my_shop_id, my_office_id):
        super().__init__(unique_id, model, pos, my_house_id, my_shop_id, my_office_id)

        # Agent systems
        self.position = CmpPosition(unique_id, pos, my_house_id, my_shop_id, my_office_id)
        self.food = CmpFood()
        self.economy = CmpEconomy()
        self.deliberation = CmpDeliberation()
        self.data_social_groups = CmpSocialGroups()

        # Deliberation and context
        self.schedule_time = CmpTimeSchedule()

        # Initialisation functions
        self.model.schedule.add(self)

    def step(self):
        # Input context-sensitive deliberation, I want the deliberator to take control over the behavior of the agent
        # this works better in python because of problems with cyclic imports, so I made a separation between data
        # and the manipulating systems
        print("#####################################")

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", "
        # info += "Money: " + str(self.economy.money) + " (" + str(self.economy.salary) + ")"
        info += ", B:" + str(self.food.beef) + ",C:" + str(self.food.chicken) + ",T:" + str(self.food.tofu)
        # info += ", Social group: " + str(self.data_social_groups.my_group)
        info += ", " + self.needs.get_str()
        return info
