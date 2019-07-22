from src.common.utils.utils import Utils


class ReportItem(object):
    def __init__(self, report_type, session_id):
        super(ReportItem, self).__init__()
        self.id = Utils.random_string_generator()
        self.params = {}
        self.report_type = str(report_type)
        self.session_id = str(session_id)
        self.timestamp = Utils.get_timestamp()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))
