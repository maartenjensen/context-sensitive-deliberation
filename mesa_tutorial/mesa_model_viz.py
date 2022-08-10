from mesa_tutorial.mesa_model import MesaShoppingModel
from mesa_tutorial.mesa_params import *

import mesa

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = mesa.visualization.ModularServer(
    MesaShoppingModel, [grid], Param.model_name, {Param.n_agents: 100, Param.width: 10, Param.height: 10})
server.port = 8521  # The default
server.launch()