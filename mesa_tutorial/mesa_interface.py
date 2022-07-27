from mesa_tutorial.mesa_model import MesaShoppingModel, MyAgent
from mesa_params import *

import mesa

def agent_portrayal(agent: MyAgent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.food > 0:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal

def mesa_start_simulation():
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    chart = mesa.visualization.ChartModule([{"Label": "Avg food", "Color": "Black"}],
                                           data_collector_name=param.datacollector)

    model_name = "Shopping model"
    server = mesa.visualization.ModularServer(
        MesaShoppingModel, [grid, chart], model_name, {"n_agents": 100, "width": 10, "height": 10}
    )
    server.port = 8521  # The default
    print("Launching server with model : " + model_name)
    server.launch()