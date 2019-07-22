import json
import random
import string
import datetime
import ntplib as ntplib
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.utils.auth_zero import AuthorizationZero


class Utils:

    @staticmethod
    @automation_logger(logger)
    def to_json(object_):
        """
        Converts a class object to JSON object.
        :param object_: a class instance.
        :return: a JSON object (python dictionary).
        """
        return json.dumps(object_, default=lambda o: vars(o), sort_keys=True, indent=4)

    @staticmethod
    @automation_logger(logger)
    def get_timestamp():
        return datetime.datetime.utcnow().isoformat() + "Z"

    @classmethod
    @automation_logger(logger)
    def get_synch_timestamp(cls, left_time_seconds=10):

        if left_time_seconds > 0:
            try:
                ntp_client = ntplib.NTPClient()
                ntp_response = ntp_client.request("time1.google.com", version=3)
                time_offset = ntp_response.offset
                return (datetime.datetime.utcnow() + datetime.timedelta(seconds=time_offset)).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ")
            except ntplib.NTPException as e:
                logger.logger.exception(F"NTPException: {e}")
                left_time_seconds -= 1
                cls.get_synch_timestamp(left_time_seconds)

    @staticmethod
    @automation_logger(logger)
    def get_auth_token():
        return AuthorizationZero.get_authorization_token()

    @staticmethod
    @automation_logger(logger)
    def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
        """
        Generates random string with chars and digits.
        :param size: string length expected (default is 8).
        :param chars: string characters consistency.
        :return: random string.
        """
        return ''.join(random.choice(chars) for _ in range(size))


# if __name__ == "__main__":
#     t_ = Utils.get_timestamp()
#     print(t_)
