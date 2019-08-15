import json
import requests
from src.common import logger
from json import JSONDecodeError
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.location_requests import LocationServiceRequest
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT


class LocationService(ServiceBase):
    def __init__(self):
        super(LocationService, self).__init__()
        self.url = self.api_base_url + "location-service/"

    @automation_logger(logger)
    def get_locations(self, client_id):
        uri = self.url + "locations"
        self.headers_without_token.update({"clientId": client_id})
        try:
            logger.logger.info(F"API Service URL is {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} get_locations failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_locations(self):
        uri = self.url + "locations"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.delete(uri, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} delete_locations failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_locations_by_id(self, location_id: str):
        uri = self.url + "locations/" + location_id
        try:
            logger.logger.info(F"API Service URL is {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} get_locations_by_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_locations(self, client_id, location):
        uri = self.url + "locations"
        self.headers_without_token.update({"clientId": client_id})
        payload = LocationServiceRequest().add_locations(location)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} add_locations failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_multiple_locations(self, client_id, location):
        uri = self.url + "locations/multiple"
        self.headers_without_token.update({"clientId": client_id})
        payload = LocationServiceRequest().add_multiple_locations(location)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} add_multiple_locations failed with error: {e}")
            raise e

    @automation_logger(logger)
    def register(self):
        uri = self.url + "register"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} register failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_version_info(self):
        uri = self.url + "version-info"
        try:
            logger.logger.info(F"API Service URL is {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} get_version_info failed with error: {e}")
            raise e
