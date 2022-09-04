from new_csd_framework.csd_context_module import ContextModule
from village_simulation.Agents.actions import Actions
from village_simulation.Agents.agents_parent import ParentAgent
from village_simulation.Agents.enums import Activity, Plan, Need, Goal
from village_simulation.Model.model_parent import ParentModel
from new_csd_framework.csd_context_ontology import Location, DefaultFood


class ContextExplorer:

    def __init__(self):

        self.cm = ContextModule()
        self.deliberation_functions = []
        self._0_location = Location.NONE
        self._0_time = -1
        self._0_activity = Activity.NONE
        self._0_plan = Plan.NONE
        self._0_need = Need.NONE
        self._0_goal = Goal.NONE
        self._1_beef = -1
        self._1_chicken = -1
        self._1_tofu = -1
        self._2_other_fav_food = DefaultFood.NONE
        self._3_beef_util = -1
        self._3_chicken_util = -1
        self._3_tofu_util = -1


    def deliberate(self, agent: ParentAgent, model: ParentModel):

        for delib_func in self.deliberation_functions:
            action, succeeded = delib_func(agent, model)
            if succeeded:
                return action, True

        return agent.default_food.NONE, False

    """ Primary information """

    def reset_0_primary_information(self):

        self._0_location = Location.NONE
        self._0_time = -1
        self._0_activity = Activity.NONE
        self._0_plan = Plan.NONE
        self._0_need = Need.NONE
        self._0_goal = Goal.NONE

    def get_0_primary_information(self, agent: ParentAgent, model: ParentModel):

        self.deliberation_functions = [self.deliberate_default_action_from_context]
        self._0_location = self.cm.get_location(agent)
        self._0_time = self.cm.get_time(model)

        if self.cm.get_activity(agent).value > -1:
            self._0_activity = self.cm.get_activity(agent)
        if self.cm.get_plan(agent).value > -1:
            self._0_plan = self.cm.get_activity(agent)
        if self.cm.get_need(agent).value > -1:
            self._0_need = self.cm.get_need(agent)
        if self.cm.get_goal(agent).value > -1:
            self._0_goal = self.cm.get_goal(agent)

    def print_0_primary_information(self):

        string = ""
        if self._0_location != Location.NONE:
            string += str(self._0_location)
        if self._0_time != -1:
            string += ", Time:" + str(self._0_time)
        if self._0_activity != Activity.NONE:
            string += ", " + str(self._0_activity)
        if self._0_plan != Plan.NONE:
            string += ", " + str(self._0_plan)
        if self._0_need != Need.NONE:
            string += ", " + str(self._0_need)
        if self._0_goal != Goal.NONE:
            string += ", " + str(self._0_goal)
        if len(self.deliberation_functions) > 0:
            string += ", " + str(self.deliberation_functions)

        return string

    """ Accesible objects """
    def reset_1_accesible_objects(self):

        self._1_beef = -1
        self._1_chicken = -1
        self._1_tofu = -1

    def get_1_accesible_objects(self, agent: ParentAgent, model: ParentModel):

        self.deliberation_functions = [self.deliberate_default_action_from_context]
        self._1_beef = agent.beef
        self._1_chicken = agent.chicken
        self._1_tofu = agent.tofu

    def print_1_accesible_objects(self):

        string = ""
        if self._1_beef > 0:
            string += ", Beef:" + str(self._1_beef)
        if self._1_chicken > 0:
            string += ", Chicken:" + str(self._1_chicken)
        if self._1_tofu > 0:
            string += ", Tofu:" + str(self._1_tofu)

        return string

    """ Imitation """
    def reset_2_imitation(self):

        self._2_other_fav_food = DefaultFood.NONE

    def get_2_imitation(self, agent: ParentAgent, model: ParentModel):

        self.deliberation_functions = [self.deliberation_imitation]
        self._2_other_fav_food = self.cm.get_default_food(agent, model)

    def print_2_imitation(self):

        string = ""
        if self._2_other_fav_food != DefaultFood.NONE:
            string = "Imitated" + str(self._2_other_fav_food)

        return string

    """ Rational choice """
    def reset_3_rational_choice(self):

        self._3_beef_util = -1
        self._3_chicken_util = -1
        self._3_tofu_util = -1

    def get_3_rational_choice(self, agent: ParentAgent, model: ParentModel):

        self.deliberation_functions = [self.deliberation_utility_selection]
        self._3_beef_util = agent.ut_beef
        self._3_chicken_util = agent.ut_chicken
        self._3_tofu_util = agent.ut_tofu

    def print_3_rational_choice(self):

        string = ""
        if self._3_beef_util > -1:
            string += ", B UT:" + str(self._3_beef_util)
        if self._3_chicken_util > -1:
            string += ", C UT:" + str(self._3_chicken_util)
        if self._3_tofu_util > -1:
            string += ", T UT:" + str(self._3_tofu_util)

        return string

    """ Deliberation methods """
    def deliberate_default_action_from_context(self, agent: ParentAgent, model: ParentModel):

        time = self._0_time
        chosen_food = DefaultFood.NONE

        if time == 6:
            chosen_food = agent.default_food
        elif time == 12:
            chosen_food = agent.default_food
        elif time == 18:
            chosen_food = agent.default_food
        else:
            return agent.actions.just_chill, True

        # check the default food and the preconditions
        if chosen_food == DefaultFood.BEEF and agent.beef > 0:  # This should be changed with self._1_beef,
            # this means that in the first iteration also amount of beef should be taken into acount.
            return agent.actions.eat_beef, True
        if chosen_food == DefaultFood.CHICKEN and agent.chicken > 0:
            return agent.actions.eat_chicken, True
        if chosen_food == DefaultFood.TOFU and agent.tofu > 0:
            return agent.actions.eat_tofu, True

        # A break to not check the following
        if self._1_beef == -1:
            return agent.actions.none_action, False

        # check if there is only one type of food available, more like rational choice
        if self._1_beef > 0 and self._1_chicken == 0 and self._1_tofu == 0:
            return agent.actions.eat_beef, True
        if self._1_beef == 0 and self._1_chicken > 0 and self._1_tofu == 0:
            return agent.actions.eat_chicken, True
        if self._1_beef == 0 and self._1_chicken == 0 and self._1_tofu > 0:
            return agent.actions.eat_tofu, True

        # Return nothing
        return agent.actions.none_action, False

    def deliberation_imitation(self, agent: ParentAgent, model: ParentModel):

        chosen_food = self._2_other_fav_food

        # check the default food and the preconditions
        if chosen_food == DefaultFood.BEEF and agent.beef > 0:
            return agent.actions.eat_beef, True
        if chosen_food == DefaultFood.CHICKEN and agent.chicken > 0:
            return agent.actions.eat_chicken, True
        if chosen_food == DefaultFood.TOFU and agent.tofu > 0:
            return agent.actions.eat_tofu, True

        return agent.actions.none_action, False

    def deliberation_utility_selection(self, agent: ParentAgent, model: ParentModel):

        # Utility selection, here
        if self._3_beef_util >= self._3_chicken_util >= self._3_tofu_util:
            if self._1_beef > 0:
                return agent.actions.eat_beef, True
            if self._1_chicken > 0:
                return agent.actions.eat_chicken, True
            if self._1_tofu > 0:
                return agent.actions.eat_tofu, True

        if self._3_beef_util >= self._3_tofu_util >= self._3_chicken_util:
            if self._1_beef > 0:
                return agent.actions.eat_beef, True
            if self._1_tofu > 0:
                return agent.actions.eat_tofu, True
            if self._1_chicken > 0:
                return agent.actions.eat_chicken, True

        if self._3_chicken_util >= self._3_beef_util >= self._3_tofu_util:
            if self._1_chicken > 0:
                return agent.actions.eat_chicken, True
            if self._1_beef > 0:
                return agent.actions.eat_beef, True
            if self._1_tofu > 0:
                return agent.actions.eat_tofu, True

        if self._3_chicken_util >= self._3_tofu_util >= self._3_beef_util:
            if self._1_chicken > 0:
                return agent.actions.eat_chicken, True
            if self._1_tofu > 0:
                return agent.actions.eat_tofu, True
            if self._1_beef > 0:
                return agent.actions.eat_beef, True

        if self._3_tofu_util >= self._3_beef_util >= self._3_chicken_util:
            if self._1_tofu > 0:
                return agent.actions.eat_tofu, True
            if self._1_beef > 0:
                return agent.actions.eat_beef, True
            if self._1_chicken > 0:
                return agent.actions.eat_chicken, True

        if self._3_tofu_util >= self._3_chicken_util >= self._3_beef_util:
            if self._1_tofu > 0:
                return agent.actions.eat_tofu, True
            if self._1_chicken > 0:
                return agent.actions.eat_chicken, True
            if self._1_beef > 0:
                return agent.actions.eat_beef, True

        # Return nothing
        return agent.actions.none_action, False