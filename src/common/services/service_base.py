from config_definitions import BaseConfig
from src.common.utils.utils import Utils


class ServiceBase:

    def __init__(self):
        self.api_base_url = BaseConfig.API_BASE_URL
        self.headers_without_token = {"Content-Type": "application/json", "accept": "*/*"}
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "accept": "*/*"
        }
        (self.past_timestamp, self.curr_timestamp, self.future_timestamp) = Utils.get_timestamps()
        (self.past_date, self.curr_date, self.future_date) = Utils.get_dates()
