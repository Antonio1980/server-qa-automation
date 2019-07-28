import json


class Entity(object):
    def __init__(self):
        super(Entity, self).__init__()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: vars(o), sort_keys=True, indent=4))
