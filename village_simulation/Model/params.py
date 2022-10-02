from enum import Enum


class Constants:
    layer_base = 0
    layer_buildings = 1
    layer_agents = 2


class Param:
    datacollector = "datacollector"
    model_name = "Shopping model"

    # Update these in the ShoppingModel(ParentModel): init
    # Also update in class ParentModel(mesa.Model):
    model_params = dict(
        world_cell_px=20,
        world_w_cell=35,
        world_h_cell=15,

        n_agents=4,
        n_houses=[2, 0, 1],
        n_shops=[0, 1, 0],
        n_offices=[0, 0, 1],
        n_neighborhoods=3,

        time_days=7,
        time_hours_day=24
    )

    world_w_px = model_params['world_cell_px'] * model_params['world_w_cell']
    world_h_px = model_params['world_cell_px'] * model_params['world_h_cell']
