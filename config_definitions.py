import os
import configparser


def get_parser(config):
    parser = configparser.ConfigParser()
    with open(config, mode='r', buffering=-1, closefd=True):
        parser.read(config)
        return parser


class BaseConfig:

    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg')
    parser = get_parser(config_file)

    API_BASE_URL = parser.get("URLS", "api_base_url")
    SLACK_URL = parser.get("URLS", "slack_url")