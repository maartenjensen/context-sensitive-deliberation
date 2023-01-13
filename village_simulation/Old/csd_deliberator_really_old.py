from math import floor

from village_simulation.EComponentsS.cmp_time_schedule import ActivityInformation
from village_simulation.DelibFramework.csd_actions import ActChill, Action
from village_simulation.DelibCustom.Actions.csd_actions_custom import ActNone, ActSleep, ActWork, ActEatBeef, ActEatChicken, \
    ActEatTofu, ActTravelToWork, ActTravelToHome, ActTravelToShop, ActBuyFood, ActBuyCar
from village_simulation.EntitiesCS.the_agent import Human
from village_simulation.EComponentsS.simulation_enums import Activity, Urgency, Origin, LocationEnum, DefaultFood, SocialGroups, \
    Goal, CarTypes
from village_simulation.Common.sim_utils import SimUtils

""" The deliberator class contains all the deliberation functions, it explores the context and calls
    the deliberation functions to help with decision making """


class Deliberator:

    def __init__(self):
        print("Initialize deliberator")

        # TODO this stuff should go into its own class (e.g. an action class so that instead of self.actNone its
        # possible to do actions.actNone, however I have to see how initialize this stuff
        self.actNone = ActNone()
        self.actChill = ActChill(0)
        self.actSleep = ActSleep(30)
        self.actWork = ActWork()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()
        self.actTravelToHome = ActTravelToHome()
        self.actTravelToWork = ActTravelToWork()
        self.actTravelToShop = ActTravelToShop()

    def deliberate(self, agent: Human):

        """ All the state variables """
        """ It should not be linear, more like state based, but how do you make this? """
        current_action = agent.deliberation.current_action
        current_plan = None
        activities_inf = []
        available_actions = None

        # Find activities
        """ State 0: check whether there is already an active action or plan or something like this """
        if isinstance(current_action, Action):
            current_action.action_step(agent)
            return

        """ State 1: no active action or plan, then lets figure out what the activity is """
        print("Figure out what the activity is")
        activities_inf.extend(self.get_typical_activity_from_location(agent))
        activities_inf.extend(self.get_typical_activity_from_time())
        activities_inf.extend(self.get_activity_from_needs(agent))

        print("Print potential activities for agent")

        string = ""
        for act_inf in activities_inf:
            string += str(act_inf.activity) + ", "
        print(string)

        print("Filter activities")
        chosen_activity_inf = None
        if len(activities_inf) == 0:
            print("Search for more activities")
        elif len(activities_inf) == 1:
            chosen_activity_inf = activities_inf.pop()
        else:
            chosen_activity_inf = self.get_activity_from_multiple_activities(activities_inf)

        if chosen_activity_inf is not None:
            print("Chosen activity:" + str(chosen_activity_inf.activity))
        else:
            print("No chosen activity")

    def get_activity_from_multiple_activities(self, activities_inf):

        check_activity = Activity.NONE
        saved_activity_inf = None
        # Check for a single activity
        for activity_inf in activities_inf:
            if check_activity == Activity.NONE:
                check_activity = activity_inf.activity
                saved_activity_inf = activity_inf
            elif check_activity != activity_inf.activity:
                return None

        return saved_activity_inf

    def get_typical_activity_from_location(self, human: Human) -> []:

        activities = []
        loc_type = human.position.location_type
        if loc_type == LocationEnum.SHOP:
            return [ActivityInformation(Activity.BUY_FOOD)]
        elif loc_type == LocationEnum.WORK:
            return [ActivityInformation(Activity.WORK)]
        # elif loc_type == LocationEnum.HOME:
        #    return [ActivityInformation(Activity.LEISURE)]
        return activities

    def get_typical_activity_from_time(self) -> []:

        # TODO include working day
        # Agents could have certain anchor points, e.g. an agent likes to start working at
        activities = []
        time = SimUtils.get_model().get_time_day()
        if 0 <= time <= 8 or time >= 22:
            activities.append(ActivityInformation(Activity.SLEEP))
        if 5 <= time <= 8 or 11 <= time <= 14 or 17 <= time <= 20:
            activities.append(ActivityInformation(Activity.EAT))
        if 6 <= time <= 9 or 16 <= time <= 19:
            activities.append(ActivityInformation(Activity.COMMUTE))
        if 7 <= time <= 18:
            activities.append(ActivityInformation(Activity.WORK))
        if 18 <= time <= 20:
            activities.append(ActivityInformation(Activity.BUY_FOOD))
        if 18 <= time <= 23:
            activities.append(ActivityInformation(Activity.LEISURE))
        return activities

    def get_activity_from_needs(self, human: Human) -> []:

        activities = []
        if human.needs.sleep >= 1:
            activities.append(ActivityInformation(Activity.SLEEP))
        if human.needs.work >= 1:
            activities.append(ActivityInformation(Activity.WORK))
        if human.needs.hunger >= 1:
            activities.append(ActivityInformation(Activity.EAT))
        if human.needs.food_safety >= 1:
            activities.append(ActivityInformation(Activity.BUY_FOOD))
        return activities

    def deliberate_old(self, agent: Human):

        print("Deliberating")
        """ Step 0: check whether there is already an active action """
        current_action = agent.deliberation.current_action
        if isinstance(current_action, Action):
            current_action.action_step(agent)
            return  # TODO there can be exceptions where the agent cannot do an action_step and breaks out of it

        """ Step 1: check information and retrieve activities """
        # TODO rewrite this part where the activity stems from the combination of time, location and needs
        activity_information = self.retrieve_activity_from_needs_time_location(agent)
        print("From needs, time: " + str(floor(SimUtils.get_model().get_time_day())) + ", loc: "
              + str(agent.position.location_type) + ", got: " + str(activity_information.activity))

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

        """ Step 7: find a goal from activities """
        goal_from_activity = self.get_goal_from_activity(activity_information)
        # TODO get goal in other ways, maybe from imitation??

        """ Step 8: Utility theory """
        action_from_utility = self.actNone
        if goal_from_activity == Goal.BUY_FOOD:
            action_from_utility = self.check_action_from_utility_food_buy(agent)
        elif goal_from_activity == Goal.BUY_CAR:
            action_from_utility = self.check_action_from_utility_car_buy(agent)

        if self.check_and_execute_action(agent, activity_information.activity, action_from_utility):
            return

        # TODO find a goal from preconditions and problems

        print("More deliberation is needed")

    def retrieve_activity_from_needs_time_location(self, human: Human) -> ActivityInformation:

        if human.needs.sleep > 0:
            return ActivityInformation(Activity.SLEEP)

        time = floor(SimUtils.get_model().get_time_day())
        location_type = human.position.location_type
        human.schedule_time.get_activity_based_on_time(time)

        return ActivityInformation(Activity.LEISURE)

    """ Returns whether the action was successfully performed"""

    def check_action_from_utility_food_buy(self, human: Human):

        print("Checking utility values for food buy selection")
        # Check if there is only one option
        if human.food.ut_beef > human.food.ut_chicken and human.food.ut_beef > human.food.ut_tofu:
            return ActBuyFood(human.food.buy_food_amount, 0, 0)
        if human.food.ut_chicken > human.food.ut_beef and human.food.ut_chicken > human.food.ut_tofu:
            return ActBuyFood(0, human.food.buy_food_amount, 0)
        if human.food.ut_tofu > human.food.ut_beef and human.food.ut_tofu > human.food.ut_chicken:
            return ActBuyFood(0, 0, human.food.buy_food_amount)

    """ This function should of course be rewritten to a function where it loops, actually it should be merged
        with the function above. """

    def check_action_from_utility_car_buy(self, human: Human):

        savings = human.economy.savings
        if savings < human.car.cost_audi:
            print("Not enough savings")
            return self.actNone
        elif savings < human.car.cost_audi:
            return ActBuyCar(CarTypes.VOLKSWAGEN_GOLF)
        elif savings < human.car.cost_tesla:
            if human.car.ut_audi > human.car.ut_vw_golf:
                return ActBuyCar(CarTypes.AUDI)
            else:
                return ActBuyCar(CarTypes.VOLKSWAGEN_GOLF)
        else:
            if human.car.ut_audi > human.car.ut_vw_golf and human.car.ut_audi > human.car.ut_tesla:
                return ActBuyCar(CarTypes.AUDI)
            elif human.car.ut_vw_golf > human.car.ut_audi and human.car.ut_vw_golf > human.car.ut_tesla:
                return ActBuyCar(CarTypes.VOLKSWAGEN_GOLF)
            elif human.car.ut_tesla > human.car.ut_audi and human.car.ut_tesla > human.car.ut_vw_golf:
                return ActBuyCar(CarTypes.TESLA)

        print("No car found TODO, implement values to make comparison on normative level")
        return self.actNone

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

        if activity == activity.BUY_CAR:
            print("No people to imitate from, could easily be implemented")

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
        elif activity == activity.BUY_CAR:
            print("No group related to car buying, could easily be implemented")

        return self.actNone

    def get_goal_from_activity(self, activity_information: ActivityInformation):

        print("Get goal from activity")
        if activity_information.activity == Activity.BUY_CAR:
            return Goal.BUY_CAR
        elif activity_information.activity == Activity.BUY_FOOD:
            return Goal.BUY_FOOD

        return Goal.NONE


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
