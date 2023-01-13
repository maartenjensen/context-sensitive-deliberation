from village_simulation.Building.location import Location
from village_simulation.Model.model_params import Constants


class Office(Location):

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos, (7, 3), '#fc9090', Constants.layer_buildings)
        print("Added an office " + str(unique_id))

    def to_str(self):
        info = "Office " + str(self.unique_id) + ", \n"

        return info
