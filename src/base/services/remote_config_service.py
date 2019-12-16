import os
import json
import pytest
import requests
from src.base.utils import logger
from json import JSONDecodeError
from src.base.utils.log_decorator import automation_logger
from src.base.services.service_base import ServiceBase
from src.base.services.svc_requests.request_constants import RESPONSE_TEXT
from src.base.services.svc_requests.remote_config_requests import RemoteConfigServiceRequest


class RemoteConfigService(ServiceBase):
    def __init__(self, auth_token):
        super(RemoteConfigService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.proxy_url = "api/"
        self.url = self.api_base_url + "remote-config-service/" + self.proxy_url

    @automation_logger(logger)
    def get_default_config(self):
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
            logger.logger.error(F"{e.__class__.__name__} get_default_config failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_config_by_name(self, config_name):
        uri = self.url + "files/" + config_name
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
            logger.logger.error(F"{e.__class__.__name__} get_config_by_name failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_configs(self):
        uri = self.url + "files/"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} get_configs failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_remote_config(self, remote_config):
        uri = self.url + "files/"
        try:
            payload = RemoteConfigServiceRequest().add_config(remote_config)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} add_remote_config failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_remote_config_hash(self, config_name=None):
        if config_name:
            uri = self.url + "get/hash/" + config_name
        else:
            uri = self.url + "get/hash/"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(uri, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} get_remote_config_hash failed with error: {e}")
            raise e

    @automation_logger(logger)
    @pytest.mark.skipif(os.environ.get("ENV") == "prod", reason="This test shouldn't run on production!")
    def delete_remote_config(self, config_name):
        uri = self.url + "files/" + config_name
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.delete(uri, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} delete_remote_config failed with error: {e}")
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
