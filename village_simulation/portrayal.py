from village_simulation.Agents.buildings import Location
from village_simulation.Agents.agents import MyAgent
from village_simulation.Model.params import Constants


def agent_portrayal(agent: MyAgent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.75}

    if isinstance(agent, MyAgent):
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