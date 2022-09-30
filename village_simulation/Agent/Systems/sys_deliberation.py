from village_simulation.Agent.Data.data_deliberation import AgentDataDeliberation
from village_simulation.Agent.Data.enums import Activity


class SysAgentDeliberation:

    def clear_deliberation(self, deliberation: AgentDataDeliberation):

        deliberation.current_activity = Activity.NONE
        deliberation.current_action = None
