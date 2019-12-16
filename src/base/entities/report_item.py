from src.base.utils import logger
from src.base.utils.log_decorator import automation_logger
from src.base.utils.utils import Utils
from src.base.entities.entity import Entity
from src.base.services.svc_requests.request_constants import PARAM1, PARAM2, PARAM3


class ReportItem(Entity):
    def __init__(self, report_type, session_id):
        super(ReportItem, self).__init__()
        self.id = Utils.get_random_string()
        self.params = dict()
        self.report_type = str(report_type)
        self.session_id = str(session_id)
        self.timestamp = self.curr_timestamp

    @automation_logger(logger)
    def set_config(self, *args):
        (param1, param2, param3, ) = args
        self.params[PARAM1] = param1
        self.params[PARAM2] = param2
        self.params[PARAM3] = param3
        return self
