from village_simulation.Building.location import Location
from village_simulation.Model.params import Constants


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
