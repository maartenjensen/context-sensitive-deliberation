from mesa import Agent

from village_simulation.EntitiesCS.the_agent import Human
from village_simulation.Building.location import Location
from village_simulation.Model.model_params import Constants


def agent_portrayal(agent: Agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.75}
    if isinstance(agent, Human):
        portrayal["Layer"] = Constants.layer_agents
        portrayal["Color"] = "grey"
        portrayal["Text"] = agent.to_str()
        portrayal["text"] = agent.unique_id
        portrayal["text_color"] = "White"

    elif isinstance(agent, Location):
        portrayal["Shape"] = "rect"
        portrayal["w"] = agent.dim[0]
        portrayal["h"] = agent.dim[1]
        portrayal["Color"] = agent.color
        portrayal["Layer"] = agent.layer
        portrayal["text"] = agent.to_str()
        portrayal["text_color"] = "black"

    return portrayal
