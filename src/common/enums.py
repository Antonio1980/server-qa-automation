from enum import Enum


class Environment(str, Enum):
    STAGING = "stg"
    INTEGRATION = "int"
    PRODUCTION = "prod"


class Types(str, Enum):
    CAR = "CAR"
    PEDESTRIAN = "PEDESTRIAN"
    BIKE = "BIKE"
