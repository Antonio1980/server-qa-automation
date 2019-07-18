import json
import requests
from src.common import logger
from src.common.log_decorator import automation_logger
from src.common.services.service_base import ServiceBase
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
            _response = requests.get(uri, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body, _response
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} get_endpoints failed with error: {e}")
            raise e


# if __name__ == "__main__":
#     print(RoutingService().get_endpoints())