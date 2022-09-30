from enum import Enum, auto

""" I"m putting everything in an Enum because otherwise its just being a big mess if I put enums in multiple files """


class Activity(Enum):
    NONE = auto()
    WORK = auto()
    RELAXING = auto()
    EAT = auto()
    EAT_TOGETHER = auto()
    BUY_FOOD = auto()
    BUY_CAR = auto()
    LEISURE = auto()
    SLEEP = auto()
    TRAVEL = auto()

    # To be removed
    MORNING_ROUTINE = auto()
    EAT_BEEF = auto()
    EAT_CHICKEN = auto()
    EAT_TOFU = auto()
    TRAVEL_TO_WORK = auto()
    TRAVEL_TO_HOME = auto()
    TRAVEL_TO_SHOP = auto()


class Goal(Enum):
    NONE = -1
    BUY_FOOD = 0
    BUY_CAR = 1


class Urgency(Enum):
    NONE = -1
    IMMEDIATE = 0
    SOON = 1
    WHENEVER = 2


class Origin(Enum):
    NONE = auto()
    SCHEDULE = auto()
    LOCATION = auto()


class Need(Enum):
    NONE = -1
    HUNGER = 0
    FOOD = -1


class Plan(Enum):  # Maybe this needs to contain explicit steps for the plan
    NONE = -1
    GET_FOOD = 0


class LocationEnum(Enum):
    NONE = -1
    HOME = 0
    HOUSE = 1
    OUTSIDE = 2
    SHOP = 3
    WORK = 4


class DefaultFood(Enum):
    NONE = -1
    BEEF = 0
    CHICKEN = 1
    TOFU = 2


class Days(Enum):
    NONE = -1
    MO = 1
    TU = 2
    WE = 3
    TH = 4
    FR = 5
    SA = 6
    SU = 7


class Vehicle(Enum):
    NONE = -1
    BIKE = 0
    BUS = 1
    CAR = 2


class SocialGroups(Enum):
    NONE = auto()
    VEGAN = auto()
    BEEF_EATERS = auto()
