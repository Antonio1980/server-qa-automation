import json
import requests
from src.common.utils import logger
from config_definitions import BaseConfig
from src.common.utils.log_decorator import automation_logger


class Slack:
    slack_url = BaseConfig.SLACK_URL
    headers = {"Content-Type": "application/json"}

    @classmethod
    @automation_logger(logger)
    def send_message(cls, message: str):
        data = {
            "text": message,
            "parse": "full",
            "link_names": "true"
        }
        payload = json.dumps(data).encode()
        try:
            _response = requests.post(cls.slack_url, data=payload, headers=cls.headers)
            body = _response.text
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} send_message failed with error: {e}")
            raise e
