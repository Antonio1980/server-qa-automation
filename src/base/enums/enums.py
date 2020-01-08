from enum import Enum


class Environment(str, Enum):
    STAGING = "stg"
    INTEGRATION = "int"
    PRODUCTION = "prod"
    LOCAL = "local"


class DetectedType(str, Enum):
    CAR = "CAR"
    PEDESTRIAN = "PEDESTRIAN"
    BIKE = "BIKE"


class OperationSystem(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    DARWIN = "darwin"
