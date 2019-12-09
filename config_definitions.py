import os
import configparser
from src import src_dir
from src.common.enums import Environment
from src.common.automation_error import AutomationError


def get_parser(config):
    parser = configparser.ConfigParser()
    with open(config, mode="r", buffering=-1, closefd=True):
        parser.read(config)
        return parser


def save_environment(env_dir, env_var):
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
    with open(os.path.join(env_dir + "environment.properties"), "w+") as f:
        f.write(env_var)


if "ENV" in os.environ.keys():
    environment = os.environ.__getitem__("ENV").lower()
else:
    os.environ["ENV"] = Environment.STAGING.value
    environment = Environment.STAGING.value

if environment == Environment.STAGING.value:
    environment_conf_file = "staging.cfg"
elif environment == Environment.INTEGRATION.value:
    environment_conf_file = "integration.cfg"
elif environment == Environment.PRODUCTION.value:
    environment_conf_file = "production.cfg"
else:
    error = "Environment is not detected ! Please specify environment variable 'ENV', like one of ENV=[stg, int, prod]"
    raise AutomationError(error)


class BaseConfig:

    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), environment_conf_file)
    parser = get_parser(config_file)

    EXPECTED_ENDPOINTS = parser.get("ARGS", "location_endpoints")
    LOG_FILE = parser.get("ARGS", "logger")
    CLOUD = parser.get("ARGS", "cloud")

    API_BASE_URL = parser.get("URLS", "api_base_url")
    SLACK_URL = parser.get("URLS", "slack_url")
    GITLAB_URL = parser.get("URLS", "gitlab_url")
    AUTH_ZERO = parser.get("URLS", "auth_zero")
    ELASTIC_CLOUD = parser.get("URLS", "elastic_cloud")
    ELASTIC_CLOUD_PORT = parser.get("URLS", "elastic_cloud_port")
    ELASTIC_LOCAL = parser.get("URLS", "elastic_local")
    ELASTIC_LOCAL_PORT = parser.get("URLS", "elastic_local_port")
    KIBANA_HOST = parser.get("URLS", "elastic_host")
    if CLOUD == "True":
        KIBANA = ELASTIC_CLOUD
        KIBANA_PORT = ELASTIC_CLOUD_PORT
    else:
        KIBANA = ELASTIC_LOCAL
        KIBANA_PORT = ELASTIC_LOCAL_PORT

    AUTH_ZERO_USER = parser.get("AUTOMATION", "auth_zero_user")
    AUTH_ZERO_PASSWORD = parser.get("AUTOMATION", "auth_zero_password")

    ALLURE_DIR = src_dir + parser.get("PATH", "allure_dir")
    save_environment(ALLURE_DIR, "env=" + os.environ.__getitem__("ENV").lower())
