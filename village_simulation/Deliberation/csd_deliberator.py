from village_simulation.Common.sim_utils import SimUtils
from village_simulation.Deliberation.csd_actions import DefaultActionsContainer
from village_simulation.Deliberation.csd_decision_context_graph import DecisionContext
from village_simulation.Deliberation.csd_tuple_manipulation import TupleManipulation
from village_simulation.EComponentsS.enums import Activity, MetaCriteria, Criteria
from village_simulation.EntitiesCS.the_agent import Human


class Deliberator:

    def __init__(self):

        self.defAct = DefaultActionsContainer()
        self.dc = DecisionContext()
        self.manip = TupleManipulation()
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
                self.manip.narrow_based_on_criteria(self.dc, agent, Criteria.URGENCY)
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
                self.manip.exp_activ_set_typical_habit_from_time(self.dc, self.defAct, agent)

            self.increase_agent_deliberation_cost(agent, 1)
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

    def check_and_execute_action(self, agent: Human, action) -> bool:

        if action != self.defAct.actNone:
            if action.check_preconditions(agent):
                action.execute_action(agent)
                agent.deliberation.current_action = action
                return True

        return False

    def save_agent_activity(self, agent: Human, activity: Activity):
        agent.deliberation.current_activity = activity
