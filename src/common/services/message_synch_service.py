import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT


class MessagesSynchService(ServiceBase):
    def __init__(self):
        super(MessagesSynchService, self).__init__()
        self.proxy_url = "api/"
        self.url = self.api_base_url + "messages-service/" + self.proxy_url

    @automation_logger(logger)
    def get_health(self):
        uri = self.url + "health"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_health failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_synch_run(self):
        uri = self.url + "sync/run"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_synch_run failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_synch_access(self):
        uri = self.url + "sync/access"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_synch_access failed with error: {e}")
            raise e