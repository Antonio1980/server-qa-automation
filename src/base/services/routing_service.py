import json
import requests
from src.base.utils import logger
from json import JSONDecodeError
from src.base.utils.utils import Utils
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
    def update_location_definitions(self, box, *args):
        """

        :param box: BoundingBox object.
        :param args: definition_id, priority, region.
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
            logger.logger.error(F"{e.__class__.__name__} update_location_definitions failed with error: {e}")
            raise e

    @automation_logger(logger)
    def create_location_definitions(self, box, *args):
        """

        :param box: BoundingBox object.
        :param args: provider, priority, region.
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v1/location-services/definitions"
        try:
            payload = RoutingServiceRequest().create_definitions(box, args)
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
            logger.logger.error(F"{e.__class__.__name__} create_location_definitions failed with error: {e}")
            raise e

    @automation_logger(logger)
    def delete_location_definitions(self, definition_id):
        """

        :param definition_id: ID- str.
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v1/location-services/definitions"
        try:
            payload = RoutingServiceRequest().delete_definitions(definition_id)
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
            logger.logger.error(F"{e.__class__.__name__} create_location_definitions failed with error: {e}")
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
    def get_location_services_hash(self):
        """

        :return:
        """
        uri = self.url + "v1/location-services/instances/latest-hash"
        try:
            logger.logger.info(F"API Service URL is GET- {uri}")
            _response = requests.get(url=uri, headers=self.headers_without_token)
            body = _response.text
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_location_services_hash failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_location_services_hash(self, hash_):
        """

        :return:
        """
        uri = self.url + "v1/location-services/instances/latest-hash"
        try:
            logger.logger.info(F"API Service URL is POST- {uri}")
            _response = requests.post(url=uri, data=hash_)
            body = _response.reason
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} add_location_services_hash failed with error: {e}")
            raise e

    @automation_logger(logger)
    def keep_alive(self, route, instance_id=Utils.get_random_string(),  *args):
        """

        :param route: Route object.
        :param instance_id: Random string.
        :param args: types: "CAR", "PEDESTRIAN", "BIKE"
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v2/keepalive"
        try:
            payload = RoutingServiceRequest().keep_alive(route, instance_id, args)
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
    def route_me_v4(self, location):
        """

        :param location:
        :return: tuple - (response body as text and pure HTTP response)
        """
        uri = self.url + "v4/route"
        try:
            payload = RoutingServiceRequest().route(location)
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
            logger.logger.error(F"{e.__class__.__name__} route_me_v4 failed with error: {e}")
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
