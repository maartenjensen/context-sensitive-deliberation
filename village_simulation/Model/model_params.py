from enum import Enum


class Constants:
    layer_base = 0
    layer_buildings = 1
    layer_agents = 2


class Param:
    datacollector = "datacollector"
    model_name = "Shopping model"

    world_cell_px = 20
    world_w_cell = 37
    world_h_cell = 15

    n_agents = 1
    n_houses = 9
    n_shops = 1
    n_offices = 1

    time_days = 7
    time_hours_day = 24
    time_steps_day = 12

    world_w_px = world_cell_px * world_w_cell
    world_h_px = world_cell_px * world_h_cell

    default_params = dict(
        world_cell_px=20,
        world_w_cell=37,
        world_h_cell=15,

        n_agents=1,
        n_houses=8,
        n_shops=1,
        n_offices=1,
        n_neighborhoods=3,

        time_days=7,
        time_hours_day=24,
        time_steps_day=6
    )
