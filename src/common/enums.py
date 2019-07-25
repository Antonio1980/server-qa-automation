from enum import Enum


class Environment(str, Enum):
    STAGING = "stg"
    INTEGRATION = "int"
    PRODUCTION = "prod"


class Browsers(str, Enum):
    CHROME = "chrome"
    IE = "ie"
    FIREFOX = "firefox"
    SAFARI = "safari"
    EDGE = "edge"
    OPERA = "opera"
    HTML_UNIT_WITH_JS = "html_js"


class Types(str, Enum):
    CAR = "CAR"
    PEDESTRIAN = "PEDESTRIAN"
    BIKE = "BIKE"
