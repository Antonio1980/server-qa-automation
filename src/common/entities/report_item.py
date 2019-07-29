from src.common.utils.utils import Utils
from src.common.entities.entity import Entity


class ReportItem(Entity):
    def __init__(self, report_type, session_id):
        super(ReportItem, self).__init__()
        self.id = Utils.get_random_string()
        self.params = dict()
        self.report_type = str(report_type)
        self.session_id = str(session_id)
        self.timestamp = self.curr_timestamp
