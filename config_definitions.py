import os
import configparser
from src.common.enums import Environment
from src.common.automation_error import AutomationError


def get_parser(config):
    parser = configparser.ConfigParser()
    with open(config, mode="r", buffering=-1, closefd=True):
        parser.read(config)
        return parser


if "ENV" in os.environ.keys():
    environment = os.environ.__getitem__("ENV")
else:
    os.environ["ENV"] = "stg"
    environment = "stg"

if environment.lower() == Environment.STAGING.value:
    environment_conf_file = "staging.cfg"
elif environment.lower() == Environment.INTEGRATION.value:
    environment_conf_file = "integration.cfg"
elif environment.lower() == Environment.PRODUCTION.value:
    environment_conf_file = "production.cfg"
else:
    error = "Environment is not detected ! Please specify environment variable 'ENV' (ENV=[stg, int, prod])"
    raise AutomationError(error)


class BaseConfig:

    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), environment_conf_file)
    parser = get_parser(config_file)

    EXPECTED_ENDPOINTS = parser.get("ARGS", "location_endpoints")
    LOG_FILE = parser.get("ARGS", "logger")

    API_BASE_URL = parser.get("URLS", "api_base_url")
    SLACK_URL = parser.get("URLS", "slack_url")
    GITLAB_URL = parser.get("URLS", "gitlab_url")
    AUTH_ZERO = parser.get("URLS", "auth_zero")

    AUTH_ZERO_USER = parser.get("AUTOMATION", "auth_zero_user")
    AUTH_ZERO_PASSWORD = parser.get("AUTOMATION", "auth_zero_password")
