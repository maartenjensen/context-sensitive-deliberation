from village_simulation.ECSystems.sys_position import SysPosition
from village_simulation.ECSystems.sys_time_schedule import SysScheduleTime
from village_simulation.Building.neighborhood import Neighborhood
from village_simulation.Building.house import House
from village_simulation.Building.office import Office
from village_simulation.Building.shop import Shop
from village_simulation.Building.time_indicator import TimeIndicator
from village_simulation.EComponentsS.enums import DefaultFood, Goal
from village_simulation.EntitiesCS.the_agent import Human
from village_simulation.Common.sim_utils import SimUtils


class VillageBuilder:

    def __init__(self):
        self.unique_id = -1

        self.houses = list()
        self.shops = list()
        self.offices = list()

    def build_buildings(self, n_houses, n_shops, n_offices, n_neighborhoods):

        # Create locations
        for i in range(n_neighborhoods):
            new_pos = (10 - 1 + ((10 + 1) * i), 0)
            neigh = Neighborhood(self.get_unique_id(), SimUtils.get_model(), new_pos)

            for j in range(n_houses[i]):
                new_pos = neigh.get_new_building_position(3)
                self.houses.append(House(self.get_unique_id(), SimUtils.get_model(), new_pos, neigh))

            for j in range(n_shops[i]):
                new_pos = neigh.get_new_building_position(5)
                self.shops.append(Shop(self.get_unique_id(), SimUtils.get_model(), new_pos, neigh))

            for j in range(n_offices[i]):
                new_pos = neigh.get_new_building_position(5)
                self.offices.append(Office(self.get_unique_id(), SimUtils.get_model(), new_pos, neigh))

        new_pos = (33, 14)
        TimeIndicator(self.get_unique_id(), SimUtils.get_model(), new_pos)

    def spawn_agents(self, num_agents):

        # Create agents
        for i in range(num_agents):
            random_house_id = SimUtils.get_model().random.choice(self.houses).unique_id
            random_shop_id = SimUtils.get_model().random.choice(self.shops).unique_id
            random_office_id = SimUtils.get_model().random.choice(self.offices).unique_id
            new_human = Human(self.get_unique_id(), SimUtils.get_model(), (0, 0), random_house_id, random_shop_id,
                              random_office_id)

            SysPosition.place_agent_in_house(new_human.position)
            sys_time_schedule = SysScheduleTime()
            sys_time_schedule.set_time_schedule(new_human.schedule_time)
            sys_time_schedule.specify_food_in_schedule(new_human.schedule_time, new_human.food.default_food)
            sys_time_schedule.specify_buy_in_schedule(new_human.schedule_time, new_human.food.beef,
                                                      new_human.food.chicken, new_human.food.tofu)

    def make_individual_changes_to_agents(self):

        agent_id = 9
        the_agent = SimUtils.get_agent_by_id(agent_id)
        if isinstance(the_agent, Human):
            the_agent.food.default_food = DefaultFood.CHICKEN
            the_agent.food.beef = 0
            the_agent.food.chicken = 6
            the_agent.food.tofu = 0

        agent_id = 10
        the_agent = SimUtils.get_agent_by_id(agent_id)
        if isinstance(the_agent, Human):
            the_agent.food.default_food = DefaultFood.TOFU
            the_agent.food.beef = 6
            the_agent.food.chicken = 6
            the_agent.food.tofu = 5

        agent_id = 11
        the_agent = SimUtils.get_agent_by_id(agent_id)
        if isinstance(the_agent, Human):
            the_agent.football.has_football_habit = False

            the_agent.football.football_serious = 5
            the_agent.football.football_teamplayer = 10
            the_agent.football.football_goalie = 10

            the_agent.football_goal = Goal.SOCIAL_ACTIVITY_WITH_FRIENDS

        print("Changing for some agents the internal aspects")
        # print("Stupifying agents (this means that information is removed from their schedule")
        # agent_id = 9
        # stupid_agent = SimUtils.get_agent_by_id(agent_id)
        # if isinstance(stupid_agent, Human):
        #     sys_time_schedule = SysScheduleTime()
        #     sys_time_schedule.custom_overwrite_buy_food(stupid_agent.schedule_time)
        #     print("Agent " + str(agent_id) + " forgot which food to buy")
        #
        # agent_id = 10
        # smart_agent = SimUtils.get_agent_by_id(agent_id)
        # if isinstance(smart_agent, Human):
        #     sys_time_schedule = SysScheduleTime()
        #     sys_time_schedule.custom_overwrite_buy_car(smart_agent.schedule_time)
        #     print("Agent " + str(agent_id) + " wants to buy a car in the evening")
        #
        # friend_1_id = 11
        # friend_2_id = 12
        # friend_1 = SimUtils.get_agent_by_id(friend_1_id)
        #
        # if isinstance(friend_1, Human):
        #     sys_time_schedule = SysScheduleTime()
        #     sys_time_schedule.custom_overwrite_eat_with_friend(friend_1.schedule_time, friend_2_id)
        #     print("Agent " + str(friend_1_id) + " wants to eat with Agent" + str(friend_2_id))
        #
        # friend_2 = SimUtils.get_agent_by_id(friend_2_id)
        # if isinstance(friend_2, Human):
        #     sys_time_schedule = SysScheduleTime()
        #     sys_time_schedule.custom_overwrite_eat_with_friend(friend_2.schedule_time, friend_1_id)
        #     print("Agent " + str(friend_2_id) + " wants to eat with Agent" + str(friend_1_id))


    def print_humans(self):
        for a in SimUtils.get_all_agents(False):
            if isinstance(a, Human):
                print("Human " + str(a.unique_id))
                a.schedule_time.print_schedule()

    def get_unique_id(self):
        self.unique_id += 1
        return self.unique_id
