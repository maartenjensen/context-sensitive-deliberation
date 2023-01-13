from village_simulation.EComponentsS.cmp_position import CmpPosition
from village_simulation.EComponentsS.simulation_enums import LocationEnum
from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Building.house import House
from village_simulation.Building.office import Office
from village_simulation.Building.shop import Shop


class SysPosition:

    @staticmethod
    def place_agent_in_house(position: CmpPosition):
        house = SimUtils.get_agent_by_id(position.my_house_id)
        if isinstance(house, House):
            position.pos = house.get_random_position_on()
            SimUtils.get_model().grid.place_agent(SimUtils.get_agent_by_id(position.agent_id), position.pos)
            position.location_id = position.my_house_id
            position.location_type = LocationEnum.HOME
        else:
            print(SimUtils.print_error(str(house) + " is not a house"))

    @staticmethod
    def move_to_house(position: CmpPosition):
        house = SimUtils.get_agent_by_id(position.my_house_id)
        if isinstance(house, House):
            position.pos = house.get_random_position_on()
            SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(position.agent_id), position.pos)
            position.location_id = position.my_house_id
            position.location_type = LocationEnum.HOME
        else:
            print(SimUtils.print_error(str(house) + " is not a house"))

    @staticmethod
    def move_to_shop(position: CmpPosition):
        shop = SimUtils.get_agent_by_id(position.my_shop_id)
        if isinstance(shop, Shop):
            position.pos = shop.get_random_position_on()
            SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(position.agent_id), position.pos)
            position.location_id = position.my_shop_id
            position.location_type = LocationEnum.SHOP
        else:
            print(SimUtils.print_error(str(shop) + " is not a shop"))

    @staticmethod
    def move_to_office(position: CmpPosition):
        office = SimUtils.get_agent_by_id(position.my_office_id)
        if isinstance(office, Office):
            position.pos = office.get_random_position_on()
            SimUtils.get_model().grid.move_agent(SimUtils.get_agent_by_id(position.agent_id), position.pos)
            position.location_id = position.my_office_id
            position.location_type = LocationEnum.WORK
        else:
            print(SimUtils.print_error(str(office) + " is not an office"))
