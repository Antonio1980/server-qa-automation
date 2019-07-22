import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.areas_blacklist_requests import AreasBlacklistServiceRequest


class AreasBlacklistService(ServiceBase):
    def __init__(self, auth_token):
        super(AreasBlacklistService, self).__init__()
        self.headers.update({'Authorization': 'Bearer {}'.format(auth_token)})
        self.url = self.api_base_url + "areas-blacklist-manager/api/"

    @automation_logger(logger)
    def get_areas(self):
        uri = self.url + "areas"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_areas(self, *args):
        """

        :param args: sw_lng, sw_lat, ne_lng, ne_lat
        :return:
        """
        uri = self.url + "areas"
        payload = AreasBlacklistServiceRequest().add_areas(args)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} add_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_areas(self):
        uri = self.url + "areas"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.delete(uri, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_hash(self):
        uri = self.url + "hash"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_hash failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_area(self, shape_id):
        uri = self.url + "areas/" + str(shape_id)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.delete(uri, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def export_areas(self):
        uri = self.url + "areas/export"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} export_areas failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_areas_inbox(self, sw_lng: float, sw_lat: float, ne_lng: float, ne_lat: float) -> tuple:
        uri = self.url + "areas/inBox"
        payload = AreasBlacklistServiceRequest().get_areas_inbox(sw_lng, sw_lat, ne_lng, ne_lat)
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers_without_token)
            body = json.loads(_response.text)
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
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(uri, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} activate_area failed with error: {e}")
            raise e


# if __name__ == "__main__":
#     print(AreasBlacklistService().add_areas(5, 1, 6, 0))
#     print(AreasBlacklistService().get_areas_inbox(5, 1, 6, 0))
#     print(AreasBlacklistService().activate_area("id", True))