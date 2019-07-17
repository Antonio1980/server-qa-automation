import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
from src.common.services.svc_requests.request_constants import *
from src.common.services.svc_requests.routing_requests import RoutingServiceRequest


class RoutingService(ServiceBase):
    def __init__(self):
        super(RoutingService, self).__init__()
        self.url = self.api_base_url + "routing-service/"

    @automation_logger(logger)
    def get_endpoints(self):
        """

        :return:
        """
        uri = self.url + "endpoints"
        try:
            logger.logger.info(F"API Service URL is {uri}")
            _response = requests.get(uri, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info(RESPONSE_TEXT.format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} create_api_token failed with error: {e}")
            raise e


# if __name__ == "__main__":
#     print(RoutingService().get_endpoints())