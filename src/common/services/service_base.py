from config_definitions import BaseConfig
from src.common.utils.utils import Utils


class ServiceBase:
    api_base_url = BaseConfig.API_BASE_URL
    headers_without_token = {"Content-Type": "application/json", "accept": "*/*"}
    headers = {
               "Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
               "accept": "*/*"
               }
    (past_timestamp, curr_timestamp, future_timestamp) = Utils.get_timestamps()
    (past_date, curr_date, future_date) = Utils.get_dates()
