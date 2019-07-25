import json
import requests
from src.common import logger
from src.common.entities.route import Route
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import RESPONSE_TEXT
from src.common.services.svc_requests.routing_requests import RoutingServiceRequest


class RoutingService(ServiceBase):
    def __init__(self):
        super(RoutingService, self).__init__()
        self.url = self.api_base_url + "routing-service/"

    @automation_logger(logger)
    def analytics(self, client_id, report_item):
        uri = self.url + "analytics"
        try:
            payload = RoutingServiceRequest().analytics(client_id, report_item)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} analytics failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_endpoints(self):
        uri = self.url + "endpoints"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(url=uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_endpoints failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_endpoints(self):
        uri = self.url + "endpoints"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.delete(url=uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} delete_endpoints failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_count_by_type(self):
        uri = self.url + "v1/count-by-type"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(url=uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_count_by_type failed with error: {e}")
            raise e

    @automation_logger(logger)
    def keep_alive(self, bounding_box, route, *args):
        """

        :param bounding_box: BoundingBox object.
        :param route: Route object
        :param args: types: "CAR", "PEDESTRIAN", "BIKE"
        :return: tuple - (response body as text and pure response)
        """
        uri = self.url + "v2/keepalive"
        try:
            payload = RoutingServiceRequest().keep_alive(bounding_box, route, args)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} keep_alive failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_route(self, location):
        uri = self.url + "route"
        try:
            payload = RoutingServiceRequest().add_route(location)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} add_route failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_route_v3(self, location):
        uri = self.url + "v3/route"
        try:
            payload = RoutingServiceRequest().add_route(location)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} add_route failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_route_v4(self, location):
        uri = self.url + "v4/route"
        try:
            payload = RoutingServiceRequest().add_route(location)
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
            body = "OK"
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} add_route failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_version_info(self):
        uri = self.url + "version-info"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers_without_token)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_version_info failed with error: {e}")
            raise e


# if __name__ == "__main__":
#     from src.common.entities.bounding_box import BoundingBox
#
#     box = BoundingBox().set_bounding_box(0.76823, 439824.4, 2288, 0)
#     route_ = Route().set_route("128.65.34.98", "Anton", 5, [200, 400])
#
#     print(RoutingService().keep_alive(box, route_, 1, 2, 3))
#     pass