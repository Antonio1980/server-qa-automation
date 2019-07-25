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


class OperationSystem(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    DARWIN = "darwin"


class DriverHelper(str, Enum):
    ID = "id"
    XPATH = "xpath"
    CLASS_NAME = "class_name"
    NAME = "name"
    TAG_NAME = "tag_name"
    LINK_TEXT = "link_text"
    CSS_SELECTOR = "css_selector"
    PARTIAL_LINK_TEXT = "partial_link_text"


class Types(str, Enum):
    CAR = "CAR"
    PEDESTRIAN = "PEDESTRIAN"
    BIKE = "BIKE"
