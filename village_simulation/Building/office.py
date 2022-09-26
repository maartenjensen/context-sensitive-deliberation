from village_simulation.Building.location import Location
from village_simulation.Model.params import Constants


class Office(Location):

    def __init__(self, unique_id, model, pos, neighborhood):
        super().__init__(unique_id, model, pos, (5, 5), '#fc9090', Constants.layer_buildings)
        print("Added an office " + str(unique_id))

        self.neighborhood = neighborhood

    def to_str(self):
        info = "ID:" + str(self.unique_id) + ", \n"

        return info
