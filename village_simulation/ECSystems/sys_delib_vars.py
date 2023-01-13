from village_simulation.EComponentsS.cmp_delib_vars import CmpDeliberation
from village_simulation.EComponentsS.simulation_enums import Activity


class SysDeliberation:

    @staticmethod
    def clear_deliberation(deliberation: CmpDeliberation):

        if deliberation.current_action is not None:
            if deliberation.current_action.steps_active <= 0:
                deliberation.current_activity = Activity.NONE
                deliberation.current_action = None
                # deliberation.delib_cost is NOT reset here since its used in the graph
