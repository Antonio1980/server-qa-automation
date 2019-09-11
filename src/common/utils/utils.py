import json
import time
import uuid
import random
import string
import datetime
from src.common import logger
from src.common.automation_error import AutomationError
from src.common.log_decorator import automation_logger


class Utils:

    @staticmethod
    @automation_logger(logger)
    def to_json_dumps(object_, key=None):
        """
        Converts a class object to JSON object.
        :param key: key/value pair to delete (optional).
        :param object_: a class instance.
        :return: a JSON object (python dictionary).
        """
        if key:
            return json.dumps(json.loads(json.dumps(object_, default=lambda obj: vars(obj), sort_keys=True, indent=4)
                                         ).pop(key))
        else:
            return json.dumps(object_, default=lambda obj: vars(obj), sort_keys=True, indent=4)

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

    @staticmethod
    @automation_logger(logger)
    def get_synch_timestamp(left_time_seconds=3):
        import ntplib

        if left_time_seconds > 0:

            ntp_client = ntplib.NTPClient()
            try:
                ntp_response = ntp_client.request("time.google.com", version=3)
                time_offset = ntp_response.offset
                return (datetime.datetime.utcnow() + datetime.timedelta(seconds=time_offset)).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ")
            except ntplib.NTPException as e:
                logger.logger.exception(F"NTPException: {e}")
                time.sleep(0.3)
                left_time_seconds -= 1
                return Utils.get_synch_timestamp(left_time_seconds)
