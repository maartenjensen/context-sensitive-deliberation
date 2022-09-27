from village_simulation.Agent.Data.enums import LocationEnum
from village_simulation.Common.sim_utils import SimUtils


class AgentPosition:

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
