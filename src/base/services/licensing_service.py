import json
import requests
from src.base.utils import logger
from json import JSONDecodeError
from src.base.utils.log_decorator import automation_logger
from src.base.services.service_base import ServiceBase
from src.base.services.svc_requests.licencing_service_requests import LicencingServiceRequest
from src.base.services.svc_requests.request_constants import RESPONSE_TEXT


class LicensingService(ServiceBase):
    def __init__(self, auth_token):
        super(LicensingService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.proxy_url = "api/"
        self.url = self.api_base_url + "licensing-service/" + self.proxy_url

    @automation_logger(logger)
    def get_full_config(self):
        uri = self.url + "config"
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
            logger.logger.error(F"{e.__class__.__name__} get_full_config failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_client(self, name: str, api_key: dict):
        uri = self.url + "config"
        payload = LicencingServiceRequest().add_client(name, api_key)
        try:
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
            logger.logger.error(F"{e.__class__.__name__} add_client failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_client(self, name: str):
        uri = self.url + "config"
        try:
            logger.logger.info(F"API Service URL is DELETE- {uri}")
            params = {"name": name}
            _response = requests.delete(uri, params=params, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} delete_client failed with error: {e}")
            raise e

    @automation_logger(logger)
    def validate_client(self, api_key: str, app_id: str, client_id: str):
        uri = self.url + "validate"
        payload = LicencingServiceRequest().validate(api_key, app_id, client_id)
        try:
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
            logger.logger.error(F"{e.__class__.__name__} validate_client failed with error: {e}")
            raise e
