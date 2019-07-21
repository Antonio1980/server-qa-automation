from src.common.instruments import Instruments
from src.common.services.messages_service import MessagesService
from src.common.services.remote_config_service import RemoteConfigService
from src.common.services.reporting_service import ReportingService
from src.common.services.routing_service import RoutingService
from src.common.services.areas_blacklist_service import AreasBlacklistService

auth_token = Instruments.get_auth_token()["access_token"]


class ApiClient(object):
    def __init__(self):
        super(ApiClient, self).__init__()
        self.remote_config_svc = RemoteConfigService()
        self.messages_svc = MessagesService()
        self.reporting_svc = ReportingService()
        self.routing_svc = RoutingService(auth_token)
        self.areas_blacklist_svc = AreasBlacklistService(auth_token)
