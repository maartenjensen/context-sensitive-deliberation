from enum import Enum, auto

""" I"m putting everything in an Enum because otherwise its just being a big mess if I put enums in multiple files """


class DcElement(Enum):
    NONE = auto()
    ACTIVITY = auto()
    GOAL = auto()
    PLAN = auto()
    ACTION = auto()
    URGENCY = auto()
    OTHER = auto()


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
    COMMUTE = auto()
    FOOTBALL = auto()


class Goal(Enum):
    NONE = auto()
    BUY_FOOD = auto()
    BUY_CAR = auto()
    EAT_WITH_FRIEND = auto()
    EAT_FOOD = auto()
    BECOME_PROFESSIONAL_FOOTBALL_PLAYER = auto()
    SOCIAL_ACTIVITY_WITH_FRIENDS = auto()


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
    MO = 5
    TU = 6
    WE = 7
    TH = 1
    FR = 2
    SA = 3
    SU = 4


class DayType(Enum):
    NONE = auto()
    WORK = auto()
    WEEKEND = auto()
    HOLIDAY = auto()


class Vehicle(Enum):
    NONE = -1
    BIKE = 0
    BUS = 1
    CAR = 2


class SocialGroups(Enum):
    NONE = auto()
    VEGAN = auto()
    BEEF_EATERS = auto()


class CarTypes(Enum):
    NONE = auto()
    VOLKSWAGEN_GOLF = auto()
    AUDI = auto()
    TESLA = auto()
