from village_simulation.EComponentsS.enums import Goal


class CmpFootball:

    def __init__(self):

        self.football_serious = 10
        self.football_teamplayer = 2
        self.football_goalie = 5

        self.football_goal = Goal.BECOME_PROFESSIONAL_FOOTBALL_PLAYER

        self.has_football_habit = True
