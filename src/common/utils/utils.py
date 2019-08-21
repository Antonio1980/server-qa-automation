import json
import uuid
import random
import string
import datetime
from src.common import logger
from src.common.automation_error import AutomationError
from src.common.log_decorator import automation_logger
from src.common.utils.auth_zero import AuthorizationZero


class Utils:

    @staticmethod
    @automation_logger(logger)
    def to_json_dumps(object_, key=None):
        """
        Converts a class object to JSON object.
        :param object_: a class instance.
        :return: a JSON object (python dictionary).
        """
        if key:
            return json.dumps(json.loads(json.dumps(object_, default=lambda o: vars(o), sort_keys=True, indent=4)).pop(key))
        else:
            return json.dumps(object_, default=lambda o: vars(o), sort_keys=True, indent=4)

    @staticmethod
    @automation_logger(logger)
    def get_timestamps():
        """
        Makes two timestamp integers.
        :return: past_timestamp- str (1 year back from now),
        curr_timestamp- str (current date), future_timestamp- str (future date 1 month forward)
        """
        past_timestamp = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).isoformat() + "Z"
        curr_timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        future_timestamp = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat() + "Z"
        return past_timestamp, curr_timestamp, future_timestamp

    @staticmethod
    @automation_logger(logger)
    def get_dates():
        past_date = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S") + \
                    ".918 +00:00"
        curr_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + ".918 +00:00"
        future_date = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S") + \
                    ".918 +00:00"
        return past_date, curr_date, future_date

    @staticmethod
    @automation_logger(logger)
    def get_auth_token():
        return AuthorizationZero.get_authorization_token()

    @staticmethod
    @automation_logger(logger)
    def get_random_string(size=8, chars=string.ascii_lowercase + string.digits):
        """
        Generates random string with chars and digits.
        :param size: string length expected (default is 8).
        :param chars: string characters consistency.
        :return: random string.
        """
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    @automation_logger(logger)
    def get_uuid():
        try:
            uuid_ = str(uuid.uuid4())
            logger.logger.info(f"The given UUID is: {uuid_}")
            return uuid_
        except Exception as e:
            logger.logger.error(f"{e}")
            raise AutomationError("Failed to get UUID.")
