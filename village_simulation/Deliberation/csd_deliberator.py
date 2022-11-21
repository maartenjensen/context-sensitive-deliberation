from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Deliberation.actions import ActNone, ActSleep, ActEatBeef, ActEatChicken, ActEatTofu, ActWork, \
    Action, ActBuyFood, ActRelax, ActFootballGoalie, ActFootballTeamplayer, ActFootballSeriousPlayer
from village_simulation.Deliberation.csd_decision_context import DecisionContext, Urgency
from village_simulation.EComponentsS.enums import Activity, Goal, DefaultFood, DayType, MetaCriteria, Criteria
from village_simulation.EntitiesCS.the_agent import Human


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
        """
        Returns nothing as the function itself performs the action when an action has been found
        """

        self.dc = DecisionContext()
        # chosen_action = self.actNone
        # chosen_activity = Activity.NONE
        self.reset_agent_deliberation_cost(agent)

        failed_actions = []

        counter = 1
        while counter <= 4:  # This should be
            meta_criteria = self.select_meta_criteria()
            print(meta_criteria)
            """ Urgency check """
            if meta_criteria == MetaCriteria.NARROW_ACTIVITIES:
                print("-- Narrow activities")
                self.narrow_based_on_criteria(agent, Criteria.URGENCY)
            elif meta_criteria == MetaCriteria.NARROW_GOALS:
                print("-- Narrow goals")
            elif meta_criteria == MetaCriteria.NARROW_PLANS:
                print("-- Narrow plans")
            elif meta_criteria == MetaCriteria.NARROW_ACTIONS:
                print("-- Narrow actions")
            elif meta_criteria == MetaCriteria.EXPAND_ACTIONS:
                print("-- Expand actions")
            elif meta_criteria == MetaCriteria.EXPAND_PLANS:
                print("-- Expand plans")
            elif meta_criteria == MetaCriteria.EXPAND_GOALS:
                print("-- Expand goals")
            elif meta_criteria == MetaCriteria.EXPAND_ACTIVITIES:
                print("-- Expand activities")
                print("Based on current time: " + str(SimUtils.get_model().get_time_day()))
                self.increase_agent_deliberation_cost(agent, 1)
                self.exp_activ_set_typical_habit_from_time(agent)

            self.dc.print_all()

            """ CHECK for an action """
            if self.dc.has_one_action():
                if self.check_can_perform_action(agent):
                    return
                else:
                    failed_actions.append(self.dc.get_one_action_if_one())

            counter += 1

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

    def select_meta_criteria(self) -> MetaCriteria:

        if self.dc.is_empty():
            return MetaCriteria.EXPAND_ACTIVITIES
        if self.dc.has_more_than_one_of_type(Activity):
            return MetaCriteria.NARROW_ACTIVITIES
        return MetaCriteria.EXPAND_ACTIVITIES

    def reset_agent_deliberation_cost(self, agent: Human):
        agent.deliberation.delib_cost = 0

    def increase_agent_deliberation_cost(self, agent: Human, deliberation_cost: int):
        agent.deliberation.delib_cost += deliberation_cost

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

    # ===========================================
    #   Narrow down
    # ===========================================

    def narrow_based_on_criteria(self, agent: Human, criteria: Criteria):

        print("Narrow based on criteria")
        if criteria == criteria.URGENCY:
            self.set_urgency_of_activities(agent)

            most_urgent_activities = self.get_most_urgent_activities()
            if len(most_urgent_activities) == 1:
                most_urgent_activity = most_urgent_activities[0]
                self.dc.deactivate_other_activities_and_related(most_urgent_activity)
            self.dc.print_all()

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

    # ===========================================
    #   Expand activities
    # ===========================================

    def exp_activ_set_typical_habit_from_time(self, agent: Human):

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
