import json
import requests
from src.base.utils import logger
from json import JSONDecodeError
from src.base.utils.log_decorator import automation_logger
from src.base.services.service_base import ServiceBase
from src.base.services.svc_requests.request_constants import RESPONSE_TEXT
from src.base.services.svc_requests.routing_requests import RoutingServiceRequest


class RoutingService(ServiceBase):
    def __init__(self, auth_token):
        super(RoutingService, self).__init__()
        if auth_token:
            self.headers.update({'Authorization': 'Bearer {0}'.format(auth_token)})
        self.url = self.api_base_url + "routing-service/"

    @automation_logger(logger)
    def get_location_service_configuration(self):
        """

        :return:
        """
        uri = self.url + "v1/location-service-configuration"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(url=uri, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} get_location_service_configuration failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_location_service_configuration(self):
        """

        :return:
        """
        uri = self.url + "v1/location-service-configuration"
        try:
            payload = RoutingServiceRequest().add_service_configuration()
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} add_location_service_configuration failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_location_services_v1(self):
        """

        :return:
        """
        uri = self.url + "v1/location-services"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(url=uri, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} get_location_services_v1 failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_location_services_configuration(self):
        """

        :return:
        """
        uri = self.url + "v1/location-service-configuration"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(url=uri, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} get_location_services_v1 failed with error: {e}")
            raise e

    @automation_logger(logger)
    def create_location_instance(self, region):
        """
        TODO: waiting implementation on int.
        :param region:
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v1/location-services/instances/" + region
        try:
            payload = RoutingServiceRequest().create_instance(region)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} keep_alive failed with error: {e}")
            raise e

    @automation_logger(logger)
    def update_location_definitions(self, box, *args):
        """

        :param box: BoundingBox object.
        :param args: types: definition_id, priority, region.
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v1/location-services/definitions"
        try:
            payload = RoutingServiceRequest().update_definitions(box, args)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} keep_alive failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_count_by_type_v2(self):
        """

        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v2/count-by-type"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(url=uri, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} get_count_by_type_v2 failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_count_by_type_v1(self):
        """

        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v1/count-by-type"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(url=uri, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} get_count_by_type_v2 failed with error: {e}")
            raise e

    @automation_logger(logger)
    def keep_alive(self, route, *args):
        """

        :param route: Route object.
        :param args: types: "CAR", "PEDESTRIAN", "BIKE"
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v2/keepalive"
        try:
            payload = RoutingServiceRequest().keep_alive(route, args)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers)
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
            logger.logger.error(F"{e.__class__.__name__} keep_alive failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_route_v3(self, location):
        """

        :param location:
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v3/route"
        try:
            payload = RoutingServiceRequest().add_route(location)
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=payload, headers=self.headers_without_token)
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
            logger.logger.error(F"{e.__class__.__name__} add_route_v3 failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_version_info(self):
        """

        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "version-info"
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
            logger.logger.error(F"{e.__class__.__name__} get_version_info failed with error: {e}")
            raise e

    @automation_logger(logger)
    def health(self):
        """

        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "actuator/health"
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
