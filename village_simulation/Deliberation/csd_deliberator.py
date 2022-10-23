from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Deliberation.actions import ActNone, ActSleep, ActEatBeef, ActEatChicken, ActEatTofu, ActWork, \
    Action, ActBuyFood, ActRelax, ActFootballGoalie, ActFootballTeamplayer, ActFootballSeriousPlayer
from village_simulation.Deliberation.csd_decision_context import DecisionContext, Urgency, Utility
from village_simulation.EComponentsS.enums import Activity, Goal, DefaultFood, DayType
from village_simulation.EntitiesCS.the_agent import Human


# https://groups.google.com/g/networkx-discuss/c/dZfKl6u7P5A?hl=en&pli=1
# networkx for graph structure

class Deliberator:

    def __init__(self):
        self.actNone = ActNone()
        self.actSleep = ActSleep()
        self.actEatBeef = ActEatBeef()
        self.actEatChicken = ActEatChicken()
        self.actEatTofu = ActEatTofu()
        self.actWork = ActWork()
        self.actBuyFood = ActBuyFood(6, 6, 6)
        self.actRelax = ActRelax()
        self.actFootballGoalie = ActFootballGoalie()
        self.actFootballTeamplayer = ActFootballTeamplayer()
        self.actFootballSeriousPlayer = ActFootballSeriousPlayer()

        self.dc = DecisionContext()
        print("Initialize deliberator")

    def deliberate(self, agent: Human):

        self.dc = DecisionContext()
        #chosen_action = self.actNone
        #chosen_activity = Activity.NONE
        self.reset_agent_deliberation_cost(agent)

        failed_actions = []

        """ Urgency check """
        print("1. Retrieve habits based on time " + str(SimUtils.get_model().get_time_day()))
        self.increase_agent_deliberation_cost(agent, 1)
        self.set_typical_habit_from_time(agent)
        self.dc.print_all()
        """ CHECK for an action """
        if self.dc.has_one_action():
            if self.check_can_perform_action(agent):
                return
            else:
                failed_actions.append(self.dc.get_one_action_if_one())

        """ Urgency check """
        if self.dc.has_more_than_one_activities():
            print("2.1 Check urgency of activities")
            self.increase_agent_deliberation_cost(agent, 1)
            self.set_urgency_of_activities(agent)
            self.dc.print_all()
            print("2.2 Filter on activity with highest urgency")
            most_urgent_activities = self.get_most_urgent_activities()
            if len(most_urgent_activities) == 1:
                most_urgent_activity = most_urgent_activities[0]
                self.dc.deactivate_other_activities_and_related(most_urgent_activity)
            self.dc.print_all()
            """ CHECK for an action """
            if self.dc.has_one_action():
                if self.check_can_perform_action(agent):
                    return
                else:
                    failed_actions.append(self.dc.get_one_action_if_one())

        print("3.1 expanding actions")
        if not self.dc.has_more_than_one_of_type(Action):
            self.expand_actions()
            self.dc.print_all()
            self.increase_agent_deliberation_cost(agent, 1)

        if self.dc.has_more_than_one_of_type(Action) and not self.has_football_activity_exception():

            self.increase_agent_deliberation_cost(agent, 1)
            print("3.1 set utility of actions")
            self.set_utility_of_actions(agent, failed_actions)
            self.dc.print_all()
            actions = self.get_ordered_on_utility_actions()
            for chosen_action in actions:
                if self.check_can_perform_action_selected(agent, chosen_action):
                    return
                else:
                    failed_actions.append(chosen_action)

            self.dc.print_all()

        print("4.1 Expansion of goals for football")
        self.expand_goals()
        self.dc.print_all()
        self.increase_agent_deliberation_cost(agent, 1)

        print("4.2 Abstraction of game theoretical approach to selecting which based on the goal")
        self.increase_agent_deliberation_cost(agent, 3)
        self.select_action_from_goal()
        if self.dc.has_one_action():
            if self.check_can_perform_action(agent):
                return
            else:
                failed_actions.append(self.dc.get_one_action_if_one())

        # # Perform action
        # if self.dc.has_one_action():
        #     action_id = self.dc.get_one_action_id()
        #     chosen_action = self.dc.get_object_from_id(action_id)
        #     chosen_activity = self.dc.get_related_activities(action_id)
        #
        #     if self.check_and_execute_action(agent, chosen_action):
        #         self.save_agent_activity(agent, chosen_activity)
        #         return

        print("More deliberation is needed")

    def check_can_perform_action(self, agent: Human) -> bool:

        chosen_action = self.dc.get_one_action_if_one()
        related_activities = self.dc.get_related_activities(chosen_action)
        chosen_activity = Activity.NONE
        if len(related_activities) > 0:
            chosen_activity = self.dc.get_related_activities(chosen_action)

        print("--- CHECKING AND EXECUTING ACTION: " + chosen_action.to_string())
        if self.check_and_execute_action(agent, chosen_action):
            self.save_agent_activity(agent, chosen_activity)
            return True
        return False

    def check_can_perform_action_selected(self, agent: Human, chosen_action: Action) -> bool:

        related_activities = self.dc.get_related_activities(chosen_action)
        chosen_activity = Activity.NONE
        if len(related_activities) > 0:
            chosen_activity = self.dc.get_related_activities(chosen_action)

        print("--- CHECKING AND EXECUTING ACTION: " + chosen_action.to_string())
        if self.check_and_execute_action(agent, chosen_action):
            self.save_agent_activity(agent, chosen_activity)
            return True
        return False

    def reset_agent_deliberation_cost(self, agent: Human):
        agent.deliberation.delib_cost = 0

    def increase_agent_deliberation_cost(self, agent: Human, deliberation_cost: int):
        agent.deliberation.delib_cost += deliberation_cost

    def set_typical_habit_from_time(self, agent: Human):

        # These variables could be customizable dependent on the agents preference

        time = SimUtils.get_model().get_time_day()
        if 0 <= time <= 8 or time >= 22:
            self.add_habit_sleeping()
        if 5 <= time <= 8 or 11 <= time <= 14 or 17 <= time <= 20:
            self.add_habit_eat(agent)
        if 18 <= time <= 20:
            self.set_habit_buy_food()
        if SimUtils.get_model().get_day_type() is DayType.WORK:
            if 18 <= time <= 23:
                self.set_habit_leisure()
            if 7 <= time <= 18:
                self.set_habit_work()
        else:
            if 7 <= time <= 23:
                self.set_habit_leisure()
            if 8 <= time <= 11:
                if agent.football.has_football_habit:
                    self.set_habit_football()
                else:
                    self.set_activity_football()

    def has_football_activity_exception(self):

        for activity_node in self.dc.get_all_nodes_of_type(Activity):
            if activity_node == Activity.FOOTBALL:
                return True
        return False

    def expand_goals(self):

        for activity_node in self.dc.get_all_nodes_of_type(Activity):
            if activity_node == Activity.FOOTBALL:
                self.dc.add_node_and_edge(Goal.SOCIAL_ACTIVITY_WITH_FRIENDS, activity_node)
                self.dc.add_edge(self.actFootballSeriousPlayer, Activity.FOOTBALL)
                self.dc.add_edge(self.actFootballTeamplayer, Activity.FOOTBALL)
                self.dc.add_edge(self.actFootballGoalie, Activity.FOOTBALL)

    def select_action_from_goal(self):

        """ This function is very abstracted, it represents the result of a possible game theoretic approach
         Where the friends of the agents are considered and the preferences of the agent itself, returning one
         action. This is simplified by just predetermining the action, deleting the rest of the actions
         In this example the player has to be goalie because the friends want to play serious and practice their
         kicks on the goal, therefore needing the third friend to be a goalie. """
        for goal_node in self.dc.get_all_nodes_of_type(Goal):
            if goal_node == Goal.SOCIAL_ACTIVITY_WITH_FRIENDS:
                self.dc.my_dc.remove_node(self.actFootballSeriousPlayer)
                self.dc.my_dc.remove_node(self.actFootballTeamplayer)

    def expand_actions(self):

        for goal_node in self.dc.get_all_nodes_of_type(Goal):
            if goal_node == Goal.EAT_FOOD:
                self.dc.add_node_and_edge(self.actEatChicken, goal_node)
                self.dc.add_edge(self.actEatChicken, Activity.EAT)
                self.dc.add_node_and_edge(self.actEatTofu, goal_node)
                self.dc.add_edge(self.actEatTofu, Activity.EAT)
                self.dc.add_node_and_edge(self.actEatBeef, goal_node)
                self.dc.add_edge(self.actEatBeef, Activity.EAT)

    def set_utility_of_actions(self, agent: Human, failed_actions: []):

        for action_node in self.dc.get_all_nodes_of_type(Action):
            if action_node in failed_actions:
                self.dc.add_node_and_edge(Utility(-1000), action_node)
            elif action_node == self.actEatChicken:
                self.dc.add_node_and_edge(Utility(agent.food.ut_chicken), action_node)
            elif action_node == self.actEatBeef:
                self.dc.add_node_and_edge(Utility(agent.food.ut_beef), action_node)
            elif action_node == self.actEatTofu:
                self.dc.add_node_and_edge(Utility(agent.food.ut_tofu), action_node)
            elif action_node == self.actFootballSeriousPlayer:
                self.dc.add_node_and_edge(Utility(agent.football.football_serious), action_node)
            elif action_node == self.actFootballTeamplayer:
                self.dc.add_node_and_edge(Utility(agent.football.football_teamplayer), action_node)
            elif action_node == self.actFootballGoalie:
                self.dc.add_node_and_edge(Utility(agent.football.football_goalie), action_node)

    def set_urgency_of_activities(self, agent: Human):

        for activity_node in self.dc.get_all_nodes_of_type(Activity):
            if activity_node == Activity.SLEEP:
                self.dc.add_node_and_edge(Urgency(agent.needs.sleep), activity_node)
            elif activity_node == Activity.EAT:
                self.dc.add_node_and_edge(Urgency(agent.needs.hunger), activity_node)
            elif activity_node == Activity.WORK:
                self.dc.add_node_and_edge(Urgency(agent.needs.work), activity_node)
            elif activity_node == Activity.BUY_FOOD:
                self.dc.add_node_and_edge(Urgency(agent.needs.food_safety), activity_node)
            elif activity_node == Activity.LEISURE:
                self.dc.add_node_and_edge(Urgency(agent.needs.leisure), activity_node)
            elif activity_node == Activity.FOOTBALL:
                self.dc.add_node_and_edge(Urgency(2), activity_node)  # Hardcoded high value since football is planned

    def get_most_urgent_activities(self) -> []:

        highest = -1.0
        highest_object = None
        for urgency_node in self.dc.get_all_nodes_of_type(Urgency):
            if isinstance(urgency_node, Urgency):
                if urgency_node.get_urgency_amount() > highest or highest_object is None:
                    highest = urgency_node.get_urgency_amount()
                    highest_object = urgency_node

        if highest_object is None:
            return []
        else:
            return self.dc.get_related_activities(highest_object)

    """ TODO put this function in the decision context class """
    def get_ordered_on_utility_actions(self) -> []:

        ordered_actions = []
        utility_nodes = self.dc.get_all_nodes_of_type(Utility)
        amount_of_actions = len(utility_nodes)
        while len(ordered_actions) < amount_of_actions:
            highest = -100000000.0
            highest_utilities = []
            for utility_node in utility_nodes:
                if isinstance(utility_node, Utility):
                    amount = utility_node.get_amount()
                    if amount > highest or utility_node is None:
                        highest = amount
                        highest_utilities = [utility_node]
                    elif utility_node.get_amount() == highest:
                        highest_utilities.append(utility_node)

            print(highest_utilities)
            for highest_utility in highest_utilities:
                action = self.dc.get_related_actions(highest_utility)[0]
                if action not in ordered_actions:
                    ordered_actions.append(action)
                    utility_nodes.remove(highest_utility)

        print(ordered_actions)
        return ordered_actions

    def add_habit_sleeping(self):

        self.dc.add_node(Activity.SLEEP)
        self.dc.add_node_and_edge(self.actSleep, Activity.SLEEP)

    def add_habit_eat(self, agent: Human):

        self.dc.add_node(Activity.EAT)
        self.dc.add_node_and_edge(Goal.EAT_FOOD, Activity.EAT)
        if agent.food.default_food == DefaultFood.BEEF:
            self.dc.add_node_and_edge(self.actEatBeef, Activity.EAT)
        elif agent.food.default_food == DefaultFood.CHICKEN:
            self.dc.add_node_and_edge(self.actEatChicken, Activity.EAT)
        elif agent.food.default_food == DefaultFood.TOFU:
            self.dc.add_node_and_edge(self.actEatTofu, Activity.EAT)
        self.dc.add_edge(self.actEatChicken, Goal.EAT_FOOD)

    def set_habit_work(self):

        self.dc.add_node(Activity.WORK)
        self.dc.add_node_and_edge(self.actWork, Activity.WORK)

    def set_habit_buy_food(self):

        self.dc.add_node(Activity.BUY_FOOD)
        self.dc.add_node_and_edge(self.actBuyFood, Activity.BUY_FOOD)

    def set_habit_leisure(self):

        self.dc.add_node(Activity.LEISURE)
        self.dc.add_node_and_edge(self.actRelax, Activity.LEISURE)

    def set_habit_football(self):

        self.dc.add_node(Activity.FOOTBALL)
        self.dc.add_node_and_edge(self.actFootballSeriousPlayer, Activity.FOOTBALL)
        self.dc.add_node_and_edge(Goal.BECOME_PROFESSIONAL_FOOTBALL_PLAYER, self.actFootballSeriousPlayer)
        self.dc.add_node_and_edge(Goal.BECOME_PROFESSIONAL_FOOTBALL_PLAYER, Activity.FOOTBALL)

    def set_activity_football(self):

        self.dc.add_node(Activity.FOOTBALL)
        self.dc.add_node_and_edge(self.actFootballSeriousPlayer, Activity.FOOTBALL)
        self.dc.add_node_and_edge(self.actFootballTeamplayer, Activity.FOOTBALL)
        self.dc.add_node_and_edge(self.actFootballGoalie, Activity.FOOTBALL)

    def check_and_execute_action(self, agent: Human, action) -> bool:

        if action != self.actNone:
            if action.check_preconditions(agent):
                action.execute_action(agent)
                agent.deliberation.current_action = action
                return True

        return False

    def save_agent_activity(self, agent: Human, activity: Activity):
        agent.deliberation.current_activity = activity
