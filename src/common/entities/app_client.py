from src.common.entities.device_app import DeviceApp
from src.common.utils.utils import Utils


class AppClient(object):
    def __init__(self):
        super(AppClient, self).__init__()
        self.id = Utils.get_uuid()
        self.device = DeviceApp()

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))
