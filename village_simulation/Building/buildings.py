import math

import mesa

from village_simulation.Model.model_parent import ParentModel
from village_simulation.Model.params import Constants

""" Base class """


class Location(mesa.Agent):
    """Agent"""

    def __init__(self, unique_id, model: ParentModel, pos, dim, color, layer):
        super().__init__(unique_id, model)
        self.model = model
        self.pos = pos
        self.dim = dim
        self.color = color
        self.layer = layer

        self.model.schedule.add(self)
        self.model.grid.place_agent(self, self.pos)

    def step(self):
        a = 1 + 1

    def get_random_position_on(self):
        x = self.pos[0] - self.model.random.randint(0, self.dim[0] - 1)
        y = self.pos[1] + self.model.random.randint(0, self.dim[1] - 1)
        return x, y

    def to_str(self):
        return str(self.unique_id)


""" Child classes """


class Shop(Location):

    def __init__(self, unique_id, model: ParentModel, pos, neighborhood):
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

    def __init__(self, unique_id, model: ParentModel, pos, neighborhood):
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

    def __init__(self, unique_id, model: ParentModel, pos):
        super().__init__(unique_id, model, pos, (10, 15), '#c7c7c7', Constants.layer_base)
        print("Added a neighborhood " + str(unique_id))
        self.rel_building_x = -1
        self.rel_building_y = 1

    def get_new_building_position(self, new_building_height):
        position = self.pos[0] + self.rel_building_x, self.pos[1] + self.rel_building_y
        self.rel_building_y += new_building_height + 1
        return position


class TimeIndicator(Location):

    def __init__(self, unique_id, model: ParentModel, pos):
        super().__init__(unique_id, model, pos, (1, 1), '#cf9393', Constants.layer_base)

    def to_str(self):
        n_steps = self.model.schedule.steps
        info = str(math.floor(n_steps / self.model.time_hours_day) + 1) + " "
        day = math.floor(n_steps / self.model.time_hours_day) % self.model.time_days
        days = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
        info += days[day]
        info += ",T:"
        time = n_steps % self.model.time_hours_day
        if time < 10:
            info += "0"
        info += str(time) + ":00"
        return info
