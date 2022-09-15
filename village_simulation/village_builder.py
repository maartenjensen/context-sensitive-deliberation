from village_simulation.Building.buildings import House, Neighborhood, Shop
from village_simulation.Building.time_indicator import TimeIndicator
from village_simulation.Agent.agents import Human
from village_simulation.Model.sim_utils import SimUtils


class VillageBuilder:

    def __init__(self):
        self.unique_id = -1

        self.houses = list()

    def build_buildings(self, n_houses, n_shops, n_neighborhoods):

        # Create locations
        for i in range(n_neighborhoods):
            new_pos = (10 - 1 + ((10 + 1) * i), 0)
            neigh = Neighborhood(self.get_unique_id(), SimUtils.get_model(), new_pos)

            for j in range(n_houses[i]):
                new_pos = neigh.get_new_building_position(3)
                self.houses.append(House(self.get_unique_id(), SimUtils.get_model(), new_pos, neigh))

            for j in range(n_shops[i]):
                new_pos = neigh.get_new_building_position(5)
                Shop(self.get_unique_id(), SimUtils.get_model(), new_pos, neigh)
        new_pos = (33, 14)
        TimeIndicator(self.get_unique_id(), SimUtils.get_model(), new_pos)

    def get_unique_id(self):
        self.unique_id += 1
        return self.unique_id

    def spawn_agents(self, num_agents):

        # Create agents
        for i in range(num_agents):
            random_house = SimUtils.get_model().random.choice(self.houses)
            Human(self.get_unique_id(), SimUtils.get_model(), (0, 0), random_house)
