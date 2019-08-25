from src.common.utils.auth_zero import AuthorizationZero
from src.common.services.location_service import LocationService
from src.common.services.log_fetch_service import LogFetchService
from src.common.services.message_synch_service import MessagesSynchService
from src.common.services.messages_service import MessagesService
from src.common.services.remote_config_service import RemoteConfigService
from src.common.services.reporting_service import ReportingService
from src.common.services.routing_service import RoutingService
from src.common.services.areas_blacklist_service import AreasBlacklistService

auth_token = AuthorizationZero.get_authorization_token()["access_token"]


class ApiClient(object):
    def __init__(self):
        super(ApiClient, self).__init__()
        self.remote_config_svc = RemoteConfigService()
        self.messages_svc = MessagesService()
        self.reporting_svc = ReportingService(auth_token)
        self.routing_svc = RoutingService(auth_token)
        self.location_svc = LocationService()
        self.log_fetch_svc = LogFetchService()
        self.messages_synch_svc = MessagesSynchService()
        self.areas_blacklist_svc = AreasBlacklistService(auth_token)
