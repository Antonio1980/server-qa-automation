import time
import ntplib
import datetime
from src.common import logger
from src.common.log_decorator import automation_logger


class NtpClient(object):
    def __init__(self):
        super(NtpClient, self).__init__()
        self.ntp_client = ntplib.NTPClient()

    @automation_logger(logger)
    def get_synch_timestamp(self, left_time_seconds=10):

        if left_time_seconds > 0:
            try:
                ntp_response = self.ntp_client.request("time1.google.com", version=3)
                time_offset = ntp_response.offset
                return (datetime.datetime.utcnow() + datetime.timedelta(seconds=time_offset)).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ")
            except Exception as e:
                logger.logger.exception(F"NTPException: {e}")
                time.sleep(1.0)
                left_time_seconds -= 1
                self.get_synch_timestamp(left_time_seconds)
