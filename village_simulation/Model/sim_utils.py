from mesa import Agent

from village_simulation.Model.model_parent import ParentModel


class SimUtils:
    the_mesa_model = ParentModel()

    @staticmethod
    def set_model(model: ParentModel):
        SimUtils.the_mesa_model = model

    @staticmethod
    def get_model() -> ParentModel:
        return SimUtils.the_mesa_model

    @staticmethod
    def get_agent_by_id(unique_id: int) -> Agent:

        for agent in SimUtils.get_model().schedule.agent_buffer(shuffled=True):
            if unique_id == agent.unique_id:
                return agent
        print("Error, no agent with the following ID:" + str(unique_id))
        return None

    @staticmethod
    def print_error(string: str):
        print("ERROR:" + string)

    """ I cannot define classes here or I will get circular import"""
