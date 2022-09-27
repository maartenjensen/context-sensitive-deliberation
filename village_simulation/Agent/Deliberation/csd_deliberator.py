from village_simulation.Agent.Deliberation.new_csd_context_module import ContextTimeActivity
from village_simulation.Agent.Deliberation.actions import ActSleep, ActWork, ActChill, ActEatBeef, ActEatChicken, \
    ActEatTofu, \
    ActNone, Actions, ActTravelToHome, ActTravelToWork, ActTravelToShop
from village_simulation.Agent.Data.the_agent import Human
from village_simulation.Agent.Data.enums import Activity, Urgency, Origin
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
        time = SimUtils.get_model().get_time()
        location_type = agent.position.location_type
        activity_information = agent.schedule_time.get_activity_based_on_time(time)  # Always gives an activity
        print(
            "Time: " + str(time) + ", Loc: " + str(location_type) + ", Activity: " + str(activity_information.activity))
        # TODO activity_from_location (not relevant for now)
        # TODO insert select activity from multiple activities (e.g. higher priority)
        # Since there is only one activity
        action_from_act = self.get_action_from_activity(activity_information.activity)
        # TODO check preconditions of action
        if action_from_act != self.actNone:
            print("Execute the action")
            action_from_act.execute_action(agent)
            return

        print("More deliberation is needed")

        # self.CTimeActivity.explore_context(agent)
        # self.CTimeActivity.print_context()

        # action_object = self.get_action_from_activity(self.CTimeActivity.time_based_activity)
        # action_object.check_preconditions(agent)
        #

        # There can at some point also be multiple activities right?

    def get_action_from_activity(self, activity) -> Actions:

        if activity == Activity.SLEEP:
            return self.actSleep
        elif activity == Activity.WORK:
            return self.actWork
        elif activity == Activity.EAT:
            return self.actNone
        elif activity == Activity.LEISURE:
            return self.actChill
        elif activity == Activity.EAT_BEEF:
            return self.actEatBeef
        elif activity == Activity.EAT_CHICKEN:
            return self.actEatChicken
        elif activity == Activity.EAT_TOFU:
            return self.actEatTofu
        elif activity == Activity.TRAVEL_TO_HOME:
            return self.actTravelToHome
        elif activity == Activity.TRAVEL_TO_SHOP:
            return self.actTravelToShop
        elif activity == Activity.TRAVEL_TO_WORK:
            return self.actTravelToWork

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
