import json
import requests
from src.common import logger
from json import JSONDecodeError
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.remote_config_requests import RemoteConfigServiceRequest


class RemoteConfigService(ServiceBase):
    def __init__(self, auth_token):
        super(RemoteConfigService, self).__init__()
        self.proxy_url = "api/"
        self.url = self.api_base_url + "remote-config-service/" + self.proxy_url
        self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})

    @automation_logger(logger)
    def get_config(self):
        try:
            logger.logger.info(F"API Service URL is GET- {self.url}")
            _response = requests.get(self.url, headers=self.headers_without_token)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_config failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_remote_config(self, remote_config):
        try:
            payload = RemoteConfigServiceRequest().add_config(remote_config)
            logger.logger.info(F"API Service URL is POST- {self.url}")
            _response = requests.post(self.url, data=payload, headers=self.headers)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} set_config failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_config_hash(self):
        uri = self.url + "hash"
        try:
            logger.logger.info(F"API Service URL is GET- {self.url}")
            _response = requests.get(uri, headers=self.headers_without_token)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_config_hash failed with error: {e}")
            raise e

    @automation_logger(logger)
    def health(self):
        uri = self.url + "health"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            try:
                body = json.loads(_response.text)
            except JSONDecodeError as e:
                logger.logger.error(f"Failed to parse response json: {e}")
                if _response.text is not None:
                    body = _response.text
                else:
                    body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} health failed with error: {e}")
            raise e
