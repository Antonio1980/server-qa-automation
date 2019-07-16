from src.common.services.routing_service import RoutingService


class ApiClient(object):
    def __init__(self):
        super(ApiClient, self).__init__()
        self.routing_svc = RoutingService()
