from config_definitions import BaseConfig


class ServiceBase:
    api_base_url = BaseConfig.API_BASE_URL
    headers_without_token = {"Content-Type": "application/json", "accept": "*/*"}
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
               "accept": "*/*"
               }
