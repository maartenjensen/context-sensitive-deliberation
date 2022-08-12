from mesa_simulation.sim_model import MesaShoppingModel
from mesa_simulation.sim_agent import MyAgent, MyLocation
from mesa_simulation.sim_params import *

import mesa


def mesa_start_simulation():
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    chart = mesa.visualization.ChartModule([{"Label": "Avg food", "Color": "Black"}],
                                           data_collector_name=Param.datacollector)

    model_name = Param.model_name
    server = mesa.visualization.ModularServer(
        MesaShoppingModel, [grid, chart], model_name, Param.params_default
    )
    server.port = 8521  # The default
    print("Launching server with model : " + model_name)
    server.launch()


def agent_portrayal(agent: MyAgent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if isinstance(agent, MyAgent):
        if agent.food > 0:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2

    elif isinstance(agent, MyLocation):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0

    return portrayal