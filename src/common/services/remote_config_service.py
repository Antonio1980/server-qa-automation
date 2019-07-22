import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.remote_config_requests import RemoteConfigServiceRequest


class RemoteConfigService(ServiceBase):
    def __init__(self):
        super(RemoteConfigService, self).__init__()
        self.url = self.api_base_url + "remote-config-service/api/"

    @automation_logger(logger)
    def get_config(self):
        try:
            logger.logger.info(F"API Service URL is {self.url}")
            _response = requests.get(self.url, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_config failed with error: {e}")
            raise e

    @automation_logger(logger)
    def set_config(self):
        try:
            payload = RemoteConfigServiceRequest().set_config()
            logger.logger.info(F"API Service URL is {self.url}")
            _response = requests.post(self.url, data=payload, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} set_config failed with error: {e}")
            raise e
