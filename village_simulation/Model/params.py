from enum import Enum

class Constants:
    layer_base = 0
    layer_buildings = 1
    layer_agents = 2

class Param:

    datacollector = "datacollector"
    model_name = "Shopping model"

    model_params = dict(
        world_cell_px=20,
        world_w_cell=32,
        world_h_cell=15,

        n_agents=5,
        n_houses=[2, 0, 1],
        n_shops=[0, 1, 1],
        n_neighborhoods=3
    )

    world_w_px = model_params['world_cell_px'] * model_params['world_w_cell']
    world_h_px = model_params['world_cell_px'] * model_params['world_h_cell']
