from village_simulation.DelibFramework.csd_deliberator import Deliberator
from village_simulation.Common.sim_utils import SimUtils
from village_simulation.DelibFramework.csd_actions import Action
from village_simulation.DelibFramework.csd_decision_context_graph import DecisionContext
from village_simulation.EComponentsS.simulation_enums import Activity, MetaCriteria, Goal, Plan
from village_simulation.EntitiesCS.the_agent import Human

class DeliberatorCustom(Deliberator):

    def __init__(self):

        super().__init__()
        print("Initialized custom deliberator")

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
        while counter <= 4:
            """ Deliberate """
            meta_criteria = self.select_meta_criteria()
            print(meta_criteria)
            self.deliberation_step(agent, meta_criteria)

            # Increase deliberation cost
            self.increase_agent_deliberation_cost(agent, 1)

            # Print all
            self.dc.print_all()

            """ CHECK for an action """
            if self.dc.has_one_action():
                if self.check_can_perform_action(agent):
                    return
                else:
                    failed_actions.append(self.dc.get_one_action_if_one())

            counter += 1

    """ Specific deliberation functions """
    def deliberation_step_narrow_activities(self, agent: Human):

        print("-- Narrow activities")
        #self.tupleNarrow.
        #the_function = self.narrow_activities.pop()
        #the_function =
        #self.manip.narrow_based_on_criteria(self.dc, agent, Criteria.URGENCY)

    def deliberation_step_narrow_goals(self, agent: Human):

        print("-- Narrow goals")

    def deliberation_step_narrow_plans(self, agent: Human):

        print("-- Narrow plans")

    def deliberation_step_narrow_actions(self, agent: Human):

        print("-- Narrow actions")

    def deliberation_step_expand_actions(self, agent: Human):

        print("-- Expand actions")

    def deliberation_step_expand_plans(self, agent: Human):

        print("-- Expand plans")

    def deliberation_step_expand_goals(self, agent: Human):

        print("-- Expand plans")

    def deliberation_step_expand_activities(self, agent: Human):

        print("-- Expand activities")
        print("Based on current time: " + str(SimUtils.get_model().get_time_day()))
        #self.manip.exp_activ_set_typical_habit_from_time(self.dc, self.defAct, agent)

    """ Big deliberation functions """

    def deliberation_step(self, agent: Human, meta_criteria):

        if meta_criteria == MetaCriteria.NARROW_ACTIVITIES:
            self.deliberation_step_narrow_activities(agent)
        elif meta_criteria == MetaCriteria.NARROW_GOALS:
            self.deliberation_step_narrow_goals(agent)
        elif meta_criteria == MetaCriteria.NARROW_PLANS:
            self.deliberation_step_narrow_plans(agent)
        elif meta_criteria == MetaCriteria.NARROW_ACTIONS:
            self.deliberation_step_narrow_actions(agent)
        elif meta_criteria == MetaCriteria.EXPAND_ACTIONS:
            self.deliberation_step_expand_actions(agent)
        elif meta_criteria == MetaCriteria.EXPAND_PLANS:
            self.deliberation_step_expand_plans(agent)
        elif meta_criteria == MetaCriteria.EXPAND_GOALS:
            self.deliberation_step_expand_goals(agent)
        elif meta_criteria == MetaCriteria.EXPAND_ACTIVITIES:
            self.deliberation_step_expand_activities(agent)

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
        if self.dc.has_more_than_one_of_type(Goal):
            return MetaCriteria.NARROW_GOALS
        if self.dc.has_more_than_one_of_type(Plan):
            return MetaCriteria.NARROW_PLANS
        if self.dc.has_more_than_one_of_type(Action):
            return MetaCriteria.NARROW_ACTIONS
        if self.dc.has_zero_of_type(Action):
            return MetaCriteria.EXPAND_ACTIONS
        if self.dc.has_zero_of_type(Plan):
            return MetaCriteria.EXPAND_PLANS
        if self.dc.has_zero_of_type(Goal):
            return MetaCriteria.EXPAND_GOALS
        return MetaCriteria.EXPAND_ACTIVITIES

    """ Execution of actions """

    def check_and_execute_action(self, agent: Human, action) -> bool:

        if action != self.defAct.actNone:
            if action.check_preconditions(agent):
                action.execute_action(agent)
                agent.deliberation.current_action = action
                return True

        return False

    def save_agent_activity(self, agent: Human, activity: Activity):
        agent.deliberation.current_activity = activity

    """ DelibFramework cost """

    def reset_agent_deliberation_cost(self, agent: Human):
        agent.deliberation.delib_cost = 0

    def increase_agent_deliberation_cost(self, agent: Human, deliberation_cost: int):
        agent.deliberation.delib_cost += deliberation_cost
