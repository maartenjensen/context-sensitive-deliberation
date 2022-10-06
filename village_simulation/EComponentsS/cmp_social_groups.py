from village_simulation.EComponentsS.enums import SocialGroups
from village_simulation.Common.sim_utils import SimUtils


class CmpSocialGroups:

    def __init__(self):
        if SimUtils.get_model().random.random() < 0.9:
            self.my_group = SocialGroups.NONE
        elif SimUtils.get_model().random.random() < 0.5:
            self.my_group = SocialGroups.VEGAN
        else:
            self.my_group = SocialGroups.BEEF_EATERS
