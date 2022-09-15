import mesa

from village_simulation.Model.params import Constants
from village_simulation.Model.sim_utils import SimUtils

""" Base class """


class Location(mesa.Agent):
    """Agent"""

    def __init__(self, unique_id, model, pos, dim, color, layer):
        super().__init__(unique_id, model)
        self.pos = pos
        self.dim = dim
        self.color = color
        self.layer = layer

        SimUtils.get_model().schedule.add(self)
        SimUtils.get_model().grid.place_agent(self, self.pos)

    def step(self):
        a = 1 + 1

    def get_random_position_on(self):
        x = self.pos[0] - SimUtils.get_model().random.randint(0, self.dim[0] - 1)
        y = self.pos[1] + SimUtils.get_model().random.randint(0, self.dim[1] - 1)
        return x, y

    def to_str(self):
        return str(self.unique_id)


""" Child classes """


class Shop(Location):

    def __init__(self, unique_id, model, pos, neighborhood):
        super().__init__(unique_id, model, pos, (5, 5), '#badbc6', Constants.layer_buildings)
        print("Added a shop " + str(unique_id))

        self.neighborhood = neighborhood

        self.beef = 100
        self.chicken = 100
        self.tofu = 100

    def step(self):
        self.beef += 1
        self.chicken += 1
        self.tofu += 1

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", \n"
        info += "B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        return info


class House(Location):

    def __init__(self, unique_id, model, pos, neighborhood):
        super().__init__(unique_id, model, pos, (3, 3), '#aabcf2', Constants.layer_buildings)
        print("Added a house " + str(unique_id))

        self.neighborhood = neighborhood

        self.beef = 0
        self.chicken = 0
        self.tofu = 0

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ","
        info += "B:" + str(self.beef) + ",C:" + str(self.chicken) + ",T:" + str(self.tofu)
        return info


class Neighborhood(Location):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos, (10, 15), '#c7c7c7', Constants.layer_base)
        print("Added a neighborhood " + str(unique_id))
        self.rel_building_x = -1
        self.rel_building_y = 1

    def get_new_building_position(self, new_building_height):
        position = self.pos[0] + self.rel_building_x, self.pos[1] + self.rel_building_y
        self.rel_building_y += new_building_height + 1
        return position
