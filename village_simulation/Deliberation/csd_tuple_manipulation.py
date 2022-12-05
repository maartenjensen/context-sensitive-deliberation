from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Deliberation.csd_actions import DefaultActionsContainer
from village_simulation.Deliberation.csd_decision_context_graph import NodeUrgency, DecisionContext
from village_simulation.EComponentsS.enums import Criteria, Activity, DayType, Goal, DefaultFood
from village_simulation.EntitiesCS.the_agent import Human


# Maybe this has to be a static class
class TupleManipulation:

    def __init__(self):
        print("Init tuple manipulation")

    # ===========================================
    #   Narrow down
    # ===========================================

    def narrow_based_on_criteria(self, dc: DecisionContext, agent: Human, criteria: Criteria):

        print("Narrow based on criteria")
        if criteria == criteria.URGENCY:
            self.set_urgency_of_activities(dc, agent)

            most_urgent_activities = self.get_most_urgent_activities(dc)
            if len(most_urgent_activities) == 1:
                most_urgent_activity = most_urgent_activities[0]
                dc.deactivate_other_activities_and_related(most_urgent_activity)
            dc.print_all()

    def get_most_urgent_activities(self, dc: DecisionContext) -> []:

        highest = -1.0
        highest_object = None
        for urgency_node in dc.get_all_nodes_of_type(NodeUrgency):
            if isinstance(urgency_node, NodeUrgency):
                if urgency_node.get_urgency_amount() > highest or highest_object is None:
                    highest = urgency_node.get_urgency_amount()
                    highest_object = urgency_node

        if highest_object is None:
            return []
        else:
            return dc.get_related_activities(highest_object)

    def set_urgency_of_activities(self, dc: DecisionContext, agent: Human):

        for activity_node in dc.get_all_nodes_of_type(Activity):
            if activity_node == Activity.SLEEP:
                dc.add_node_and_edge(NodeUrgency(agent.needs.sleep), activity_node)
            elif activity_node == Activity.EAT:
                dc.add_node_and_edge(NodeUrgency(agent.needs.hunger), activity_node)
            elif activity_node == Activity.WORK:
                dc.add_node_and_edge(NodeUrgency(agent.needs.work), activity_node)
            elif activity_node == Activity.BUY_FOOD:
                dc.add_node_and_edge(NodeUrgency(agent.needs.food_safety), activity_node)
            elif activity_node == Activity.LEISURE:
                dc.add_node_and_edge(NodeUrgency(agent.needs.leisure), activity_node)
            elif activity_node == Activity.FOOTBALL:
                dc.add_node_and_edge(NodeUrgency(2),
                                     activity_node)  # Hardcoded high value since football is planned

    # ===========================================
    #   Expand activities
    # ===========================================

    def exp_activ_set_typical_habit_from_time(self, dc: DecisionContext, def_act: DefaultActionsContainer,
                                              agent: Human):

        # These variables could be customizable dependent on the agents preference
        time = SimUtils.get_model().get_time_day()
        if 0 <= time <= 8 or time >= 22:
            self.add_habit_sleeping(dc, def_act)
        if 5 <= time <= 8 or 11 <= time <= 14 or 17 <= time <= 20:
            self.add_habit_eat(dc, def_act, agent)
        if 18 <= time <= 20:
            self.set_habit_buy_food(dc, def_act)
        if SimUtils.get_model().get_day_type() is DayType.WORK:
            if 18 <= time <= 23:
                self.set_habit_leisure(dc, def_act)
            if 7 <= time <= 18:
                self.set_habit_work(dc, def_act)
        else:
            if 7 <= time <= 23:
                self.set_habit_leisure(dc, def_act)
            if 8 <= time <= 11:
                if agent.football.has_football_habit:
                    self.set_habit_football(dc, def_act)
                else:
                    self.set_activity_football(dc, def_act)

    def add_habit_sleeping(self, dc: DecisionContext, def_act: DefaultActionsContainer):

        dc.add_node(Activity.SLEEP)
        dc.add_node_and_edge(def_act.actSleep, Activity.SLEEP)

    def add_habit_eat(self, dc: DecisionContext, def_act: DefaultActionsContainer, agent: Human):

        dc.add_node(Activity.EAT)
        dc.add_node_and_edge(Goal.EAT_FOOD, Activity.EAT)
        if agent.food.default_food == DefaultFood.BEEF:
            dc.add_node_and_edge(def_act.actEatBeef, Activity.EAT)
        elif agent.food.default_food == DefaultFood.CHICKEN:
            dc.add_node_and_edge(def_act.actEatChicken, Activity.EAT)
        elif agent.food.default_food == DefaultFood.TOFU:
            dc.add_node_and_edge(def_act.actEatTofu, Activity.EAT)
        dc.add_edge(def_act.actEatChicken, Goal.EAT_FOOD)

    def set_habit_work(self, dc: DecisionContext, def_act: DefaultActionsContainer):

        dc.add_node(Activity.WORK)
        dc.add_node_and_edge(def_act.actWork, Activity.WORK)

    def set_habit_buy_food(self, dc: DecisionContext, def_act: DefaultActionsContainer):

        dc.add_node(Activity.BUY_FOOD)
        dc.add_node_and_edge(def_act.actBuyFood, Activity.BUY_FOOD)

    def set_habit_leisure(self, dc: DecisionContext, def_act: DefaultActionsContainer):

        dc.add_node(Activity.LEISURE)
        dc.add_node_and_edge(def_act.actRelax, Activity.LEISURE)

    def set_habit_football(self, dc: DecisionContext, def_act: DefaultActionsContainer):

        dc.add_node(Activity.FOOTBALL)
        dc.add_node_and_edge(def_act.actFootballSeriousPlayer, Activity.FOOTBALL)
        dc.add_node_and_edge(Goal.BECOME_PROFESSIONAL_FOOTBALL_PLAYER, def_act.actFootballSeriousPlayer)
        dc.add_node_and_edge(Goal.BECOME_PROFESSIONAL_FOOTBALL_PLAYER, Activity.FOOTBALL)

    def set_activity_football(self, dc: DecisionContext, def_act: DefaultActionsContainer):

        dc.add_node(Activity.FOOTBALL)
        dc.add_node_and_edge(def_act.actFootballSeriousPlayer, Activity.FOOTBALL)
        dc.add_node_and_edge(def_act.actFootballTeamplayer, Activity.FOOTBALL)
        dc.add_node_and_edge(def_act.actFootballGoalie, Activity.FOOTBALL)
