from village_simulation.Model.model import ShoppingModel
from village_simulation.Model.params import Param
from village_simulation.portrayal import agent_portrayal

import mesa


def mesa_start_simulation():
    grid = mesa.visualization.CanvasGrid(agent_portrayal, Param.model_params['world_w_cell'],
                                         Param.model_params['world_h_cell'], Param.world_w_px, Param.world_h_px)
    chart = mesa.visualization.ChartModule([{"Label": "Avg food", "Color": "Black"}],
                                           data_collector_name=Param.datacollector)
    chart2 = mesa.visualization.ChartModule([{"Label": "Average Deliberation Cost", "Color": "Black"}],
                                            data_collector_name=Param.datacollector)
    chart3 = mesa.visualization.ChartModule([{"Label": "Agent 1 Deliberation Cost", "Color": "Red"},
                                             {"Label": "Agent 2 Deliberation Cost", "Color": "Green"},
                                             {"Label": "Agent 3 Deliberation Cost", "Color": "Blue"}],
                                            data_collector_name=Param.datacollector)
    chart4 = mesa.visualization.ChartModule([{"Label": "Average Deliberation Cost", "Color": "Black"},
                                             {"Label": "Agent 1 Deliberation Cost", "Color": "Red"},
                                             {"Label": "Agent 2 Deliberation Cost", "Color": "Green"},
                                             {"Label": "Agent 3 Deliberation Cost", "Color": "Blue"}],
                                            data_collector_name=Param.datacollector)
    chart5 = mesa.visualization.ChartModule([{"Label": "Agent 3 Deliberation Cost", "Color": "Blue"}],
                                            data_collector_name=Param.datacollector)
    model_name = Param.model_name
    server = mesa.visualization.ModularServer(
        ShoppingModel, [grid, chart4, chart, chart2, chart3, chart5], model_name, Param.model_params
    )
    server.port = 8521  # The default
    print("Launching server with model : " + model_name)
    server.launch()
