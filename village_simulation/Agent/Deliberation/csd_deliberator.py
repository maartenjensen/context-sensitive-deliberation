from village_simulation.Agent.Data.data_time_schedule import ActivityInformation
from village_simulation.Agent.Deliberation.new_csd_context_module import ContextTimeActivity
from village_simulation.Agent.Deliberation.actions import ActSleep, ActWork, ActChill, ActEatBeef, ActEatChicken, \
    ActEatTofu, \
    ActNone, Action, ActTravelToHome, ActTravelToWork, ActTravelToShop, ActBuyFood
from village_simulation.Agent.Data.the_agent import Human
from village_simulation.Agent.Data.enums import Activity, Urgency, Origin, LocationEnum, DefaultFood
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
        if action_from_activity != self.actNone:
            if action_from_activity.check_preconditions(agent):
                action_from_activity.execute_action(agent)
                agent.deliberation.current_activity = activity_information.activity
                agent.deliberation.current_action = action_from_activity
                return

        """ Step 4: consider accessible objects and see whether they can also be used e.g. default is eat beef
         if no beef is available but chicken is available it can be chosen as well """
        # TODO check whether

        """ Step 5: imitate from people at same location (and thus same time) """
        # TODO program this now

        """ Step 6: check with collective groups """


        print("More deliberation is needed")

        # self.CTimeActivity.explore_context(agent)
        # self.CTimeActivity.print_context()

        # action_object = self.get_action_from_activity(self.CTimeActivity.time_based_activit y)
        # action_object.check_preconditions(agent)
        #

        # There can at some point also be multiple activities right?

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
            return ActBuyFood(activity_information.beef_to_buy, activity_information.chicken_to_buy,
                              activity_information.tofu_to_buy)

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
