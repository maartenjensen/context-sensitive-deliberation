from village_simulation.EComponentsS.cmp_deliberation import CmpDeliberation
from village_simulation.EComponentsS.enums import Activity


class SysDeliberation:

    @staticmethod
    def clear_deliberation(deliberation: CmpDeliberation):

        if deliberation.current_action.steps_active <= 0:
            deliberation.current_activity = Activity.NONE
            deliberation.current_action = None
