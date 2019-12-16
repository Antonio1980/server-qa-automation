import json
from src.base.utils.utils import Utils


class Entity(object):
    def __init__(self):
        super(Entity, self).__init__()
        (self.past_timestamp, self.curr_timestamp, self.future_timestamp) = Utils.get_timestamps()
        (self.past_date, self.curr_date, self.future_date) = Utils.get_dates()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda obj: vars(obj), sort_keys=True, indent=4))
