import json
import requests
from src.common.utils import logger
from json import JSONDecodeError
from src.common.utils.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.areas_blacklist_requests import AreasBlacklistServiceRequest


class AreasBlacklistService(ServiceBase):
    def __init__(self, auth_token):
        super(AreasBlacklistService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.url_proxy = "api/"
        self.url = self.api_base_url + "areas-blacklist-manager/" + self.url_proxy

    @automation_logger(logger)
    def get_areas(self):
        uri = self.url + "areas"
        try:
            logger.logger.info(F"API Service URL is GET - {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} get_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def export_areas(self):
        uri = self.url + "areas/export"
        try:
            logger.logger.info(F"API Service URL is GET - {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} export_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_areas(self, description, bounding_box):
        """
        Sends POST HTTP "AddAreas" request to AreasBlacklistService
        :param description: Any string.
        :param bounding_box: Object consists from: sw_lng, sw_lat, ne_lng, ne_lat
        :return: tuple with: body- response text as dict and pure HTTP response
        """
        uri = self.url + "areas"
        payload = AreasBlacklistServiceRequest().add_areas(description, bounding_box)
        try:
            logger.logger.info(F"API Service URL is POST - {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} add_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_areas(self):
        uri = self.url + "areas"
        try:
            logger.logger.info(F"API Service URL is DELETE- {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} delete_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_areas_by_id(self, shape_id: str):
        uri = self.url + "areas/" + shape_id
        try:
            logger.logger.info(F"API Service URL is DELETE- {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} delete_areas_by_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_areas_inbox(self, bounding_box):
        uri = self.url + "areas/inBox"
        payload = AreasBlacklistServiceRequest().get_areas_inbox(bounding_box)
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
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
            logger.logger.error(F"{e.__class__.__name__} get_areas_inbox failed with error: {e}")
            raise e

    @automation_logger(logger)
    def activate_area(self, shape_id, status):
        uri = self.url + "areas/activate"
        payload = AreasBlacklistServiceRequest().activate_area(shape_id, status)
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
            logger.logger.error(F"{e.__class__.__name__} activate_area failed with error: {e}")
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
