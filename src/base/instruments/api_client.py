from src.base.services.licensing_service import LicensingService
from src.base.services.log_fetch_service import LogFetchService
from src.base.services.message_synch_service import MessagesSyncService
from src.base.services.message_service import MessageService
from src.base.services.remote_config_service import RemoteConfigService
from src.base.services.reporting_service import ReportingService
from src.base.services.routing_service import RoutingService
from src.base.services.areas_blacklist_service import AreasBlacklistService


class ApiClient(object):

    def __init__(self, access_token=None):
        super(ApiClient, self).__init__()
        self.remote_config_svc = RemoteConfigService(access_token)
        self.message_svc = MessageService(access_token)
        self.reporting_svc = ReportingService(access_token)
        self.routing_svc = RoutingService(access_token)
        self.log_fetch_svc = LogFetchService(access_token)
        self.licensing_svc = LicensingService(access_token)
        self.messages_sync_svc = MessagesSyncService(access_token)
        self.areas_blacklist_svc = AreasBlacklistService(access_token)
