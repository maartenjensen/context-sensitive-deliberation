from village_simulation.EComponentsS.enums import LocationEnum
from village_simulation.Common.sim_utils import SimUtils


class CmpPosition:

    def __init__(self, agent_id, pos, my_house_id, my_shop_id, my_office_id):
        self.agent_id = agent_id
        self.pos = pos
        self.my_house_id = my_house_id
        self.my_shop_id = my_shop_id
        self.my_office_id = my_office_id
        self.location_id = -1
        self.location_type = LocationEnum.NONE

        self.has_bike = SimUtils.get_model().random.getrandbits(1)
        self.has_car = SimUtils.get_model().random.getrandbits(1)

    def at_home(self) -> bool:
        return self.location_id == self.my_house_id

    def at_work(self) -> bool:
        return self.location_id == self.my_office_id

    def at_shop(self) -> bool:
        return self.location_id == self.my_shop_id
