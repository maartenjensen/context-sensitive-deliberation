from village_simulation.Agent.Data.data_time_schedule import ActivityInformation
from village_simulation.Agent.Deliberation.new_csd_context_module import ContextTimeActivity
from village_simulation.Agent.Deliberation.actions import ActSleep, ActWork, ActChill, ActEatBeef, ActEatChicken, \
    ActEatTofu, \
    ActNone, Action, ActTravelToHome, ActTravelToWork, ActTravelToShop, ActBuyFood
from village_simulation.Agent.Data.the_agent import Human
from village_simulation.Agent.Data.enums import Activity, Urgency, Origin, LocationEnum, DefaultFood, SocialGroups
from village_simulation.Common.sim_utils import SimUtils

""" The deliberator class contains all the deliberation functions, it explores the context and calls
    the deliberation functions to help with decision making """


class Deliberator:

    def __init__(self):
        print("Initialize deliberator")
        # self.CTimeActivity = ContextTimeActivity()
        #
        self.actNone = ActNone()
        self.actChill = ActChill()
        self.actSleep = ActSleep()
        self.actWork = ActWork()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()
        self.actTravelToHome = ActTravelToHome()
        self.actTravelToWork = ActTravelToWork()
        self.actTravelToShop = ActTravelToShop()

    def deliberate(self, agent: Human):

        print("Deliberating")
        """ Step 1: check information and retrieve activities """
        time = SimUtils.get_model().get_time()
        location_type = agent.position.location_type
        activity_information = agent.schedule_time.get_activity_based_on_time(time)  # Always gives an activity
        print(
            "Time: " + str(time) + ", Loc: " + str(location_type) + ", Activity: " + str(activity_information.activity))

        """ Step 2: select among activities """
        # TODO activity_from_location (not relevant for now)
        # TODO insert select activity from multiple activities (e.g. higher priority)
        # Since there is only one activity

        """ Step 3: select an action from the activity """
        action_from_activity = self.get_action_from_activity(activity_information.activity)
        if action_from_activity == self.actNone:
            action_from_activity = self.get_action_from_activity_with_information(activity_information)

        # TODO check preconditions of action
        if self.check_and_execute_action(agent, activity_information.activity, action_from_activity):
            return

        """ Step 4: consider accessible objects and see whether they can also be used e.g. default is eat beef
         if no beef is available but chicken is available it can be chosen as well """
        # TODO but this can be done later its easy, just a check on what is the activity what are my options and then is there only one option

        """ Step 5: imitate from people at same location (and thus same time) """
        action_from_imitation = self.get_action_from_imitation_at_location(agent, activity_information.activity)
        if self.check_and_execute_action(agent, activity_information.activity, action_from_imitation):
            return

        """ Step 6: check with collective groups (this is just a hardcoded piece) """
        action_from_social_group = self.get_action_from_social_group(agent, activity_information.activity)
        if self.check_and_execute_action(agent, activity_information.activity, action_from_social_group):
            return

        """ Step 7: rational choice???? """
        # TODO find a goal from preconditions and problems


        print("More deliberation is needed")


    """ Returns whether the action was successfully performed"""

    def check_and_execute_action(self, agent, activity, action) -> bool:

        if action != self.actNone:
            if action.check_preconditions(agent):
                action.execute_action(agent)
                agent.deliberation.current_activity = activity
                agent.deliberation.current_action = action
                return True

        return False

    def get_action_from_activity(self, activity: Activity) -> Action:

        if activity == Activity.SLEEP:
            return self.actSleep
        elif activity == Activity.WORK:
            return self.actWork
        elif activity == Activity.EAT:
            return self.actNone
        elif activity == Activity.LEISURE:
            return self.actChill

        return self.actNone

    def get_action_from_activity_with_information(self, activity_information: ActivityInformation) -> Action:

        activity = activity_information.activity
        if activity == Activity.TRAVEL:
            if activity_information.travel_to == LocationEnum.HOME:
                return self.actTravelToHome
            elif activity_information.travel_to == LocationEnum.SHOP:
                return self.actTravelToShop
            elif activity_information.travel_to == LocationEnum.WORK:
                return self.actTravelToWork

        elif activity == Activity.EAT:
            if activity_information.food_to_eat == DefaultFood.BEEF:
                return self.actEatBeef
            elif activity_information.food_to_eat == DefaultFood.CHICKEN:
                return self.actEatChicken
            elif activity_information.food_to_eat == DefaultFood.TOFU:
                return self.actEatTofu

        elif activity == Activity.BUY_FOOD:
            if activity_information.beef_to_buy + activity_information.chicken_to_buy + activity_information.tofu_to_buy > 0:
                return ActBuyFood(activity_information.beef_to_buy, activity_information.chicken_to_buy,
                                  activity_information.tofu_to_buy)

        return self.actNone

    """ This should be implemented as taking the average of all the humans, rather than the first occurrence"""

    def get_action_from_imitation_at_location(self, human: Human, activity: Activity):

        for a in SimUtils.get_all_agents(False):
            if isinstance(a, Human):
                if a.unique_id is not human.unique_id and a.position.location_id == human.position.location_id:
                    if a.deliberation.current_action is not None and a.deliberation.current_activity == activity:
                        print("Imitating H" + str(a.unique_id) + " on action: " + str(a.deliberation.current_action))
                        return a.deliberation.current_action

        return self.actNone

    def get_action_from_social_group(self, human: Human, activity: Activity):

        print("Get action from social group:" + str(activity))
        if activity == activity.EAT:
            if human.data_social_groups.my_group == SocialGroups.VEGAN:
                return self.actEatTofu
            elif human.data_social_groups.my_group == SocialGroups.BEEF_EATERS:
                return self.actEatBeef
        elif activity == activity.BUY_FOOD:
            if human.data_social_groups.my_group == SocialGroups.VEGAN:
                return ActBuyFood(0, 0, 3)
            elif human.data_social_groups.my_group == SocialGroups.BEEF_EATERS:
                return ActBuyFood(3, 0, 0)

        return self.actNone


class ActivityHandler:

    def __init__(self):

        self.activities = [ActivityWrapper(Activity.NONE, Urgency.NONE, Origin.NONE)]
        self.activities.pop()

    def add_activity(self, activity: Activity, urgency: Urgency, origin: Origin):
        activity = ActivityWrapper(activity, urgency, origin)
        self.activities.append(activity)

    def remove_activity_by_origin(self, origin: Origin):
        temp_activities = [ActivityWrapper(Activity.NONE, Urgency.NONE, Origin.NONE)]
        temp_activities.pop()

        for act in self.activities:
            if act.origin != origin:
                temp_activities.append(act)

        self.activities = temp_activities


class ActivityWrapper:

    def __init__(self, activity: Activity, urgency: Urgency, origin: Origin):
        self.activity = activity
        self.urgency = urgency
        self.origin = origin
