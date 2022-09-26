from village_simulation.Agent.enums import DefaultFood
from village_simulation.Building.house import House
from village_simulation.Building.office import Office
from village_simulation.Building.shop import Shop
from village_simulation.Model.sim_utils import SimUtils


class AgentPosition:

    def __init__(self, agent_id, pos, my_house_id, my_shop_id, my_office_id):

        self.agent_id = agent_id
        self.pos = pos
        self.my_house_id = my_house_id
        self.my_shop_id = my_shop_id
        self.my_office_id = my_office_id
        self.location_id = -1

        self.has_bike = SimUtils.get_model().random.getrandbits(1)
        self.has_car = SimUtils.get_model().random.getrandbits(1)

    def place_agent_in_house(self):
        house = SimUtils.get_agent_by_id(self.my_house_id)
        if isinstance(house, House):
            self.pos = house.get_random_position_on()
            SimUtils.get_model().grid.place_agent(SimUtils.get_agent_by_id(self.agent_id), self.pos)
            self.location_id = self.my_house_id
        else:
            print(SimUtils.print_error(str(house) + " is not a house"))

    def move_to_house(self):
        house = SimUtils.get_agent_by_id(self.my_house_id)
        if isinstance(house, House):
            self.pos = house.get_random_position_on()
            SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(self.agent_id), self.pos)
            self.location_id = self.my_house_id
        else:
            print(SimUtils.print_error(str(house) + " is not a house"))

    def move_to_shop(self):
        shop = SimUtils.get_agent_by_id(self.my_shop_id)
        if isinstance(shop, Shop):
            self.pos = shop.get_random_position_on()
            SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(self.agent_id), self.pos)
            self.location_id = self.my_shop_id
        else:
            print(SimUtils.print_error(str(shop) + " is not a shop"))

    def move_to_office(self):
        office = SimUtils.get_agent_by_id(self.my_office_id)
        if isinstance(office, Office):
            self.pos = office.get_random_position_on()
            SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(self.agent_id), self.pos)
            self.location_id = self.my_office_id
        else:
            print(SimUtils.print_error(str(office) + " is not an office"))

    def at_home(self) -> bool:
        return self.location_id == self.my_house_id

    def at_work(self) -> bool:
        return self.location_id == self.my_office_id

    def at_shop(self) -> bool:
        return self.location_id == self.my_shop_id


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
