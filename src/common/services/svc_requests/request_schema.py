from src.common.automation_error import AutomationError
from src.common.utils.utils import Utils


class RequestSchema(object):
    timestamp = Utils.get_timestamp()
    synch_timestamp = Utils.get_synch_timestamp()
    (timestamp_from, timestamp_to) = Utils.to_timestamp()

    def __init__(self):
        super(RequestSchema, self).__init__()
        self.inner = dict()

    def __getattr__(self, name):
        if not hasattr(self, name):
            raise AutomationError('{!r} object has no attribute {!r}'.format(self.__class__, name))
        return getattr(self, name)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k[1:], v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))

    def from_json(self, key=None):
        return Utils.from_json(self, key)
