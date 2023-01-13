from village_simulation.EComponentsS.simulation_enums import CarTypes


class CmpCar:

    def __init__(self):
        self.car_type = CarTypes.NONE

        self.ut_vw_golf = 2
        self.ut_audi = 4
        self.ut_tesla = 5

        self.cost_vw_golf = 15000
        self.cost_audi = 35000
        self.cost_tesla = 40000

        self.style_vw_golf = 1
        self.style_audi = 3
        self.style_tesla = 3

        self.env_vw_golf = 2
        self.env_audi = 1
        self.env_tesla = 3
