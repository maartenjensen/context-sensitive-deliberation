import mesa

class ParentModel(mesa.Model):

    def __init__(self):
        super().__init__()
        self.grid = mesa.space.MultiGrid(10, 10, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True