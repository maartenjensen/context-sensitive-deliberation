import math

from village_simulation.Building.buildings import Location
from village_simulation.Model.model_parent import ParentModel
from village_simulation.Model.params import Constants


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