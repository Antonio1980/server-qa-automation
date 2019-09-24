from src.common.utils.auth_zero import AuthorizationZero
from src.common.services.log_fetch_service import LogFetchService
from src.common.services.message_synch_service import MessagesSyncService
from src.common.services.message_service import MessageService
from src.common.services.remote_config_service import RemoteConfigService
from src.common.services.reporting_service import ReportingService
from src.common.services.routing_service import RoutingService
from src.common.services.areas_blacklist_service import AreasBlacklistService


class ApiClient(object):
    auth_token = AuthorizationZero.get_authorization_token()["access_token"]

    def __init__(self):
        super(ApiClient, self).__init__()
        self.remote_config_svc = RemoteConfigService(self.auth_token)
        self.message_svc = MessageService(self.auth_token)
        self.reporting_svc = ReportingService(self.auth_token)
        self.routing_svc = RoutingService(self.auth_token)
        self.log_fetch_svc = LogFetchService(self.auth_token)
        self.messages_sync_svc = MessagesSyncService(self.auth_token)
        self.areas_blacklist_svc = AreasBlacklistService(self.auth_token)
