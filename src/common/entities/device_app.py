

class DeviceApp(object):
    def __init__(self, os_type="iOS", os_version="iOS 12.4", device_model="iPhone 7"):
        super(DeviceApp, self).__init__()
        self.osType = os_type
        self.osVersion = os_version
        self.deviceModel = device_model
        self.appVersion = "0.9.0.0 INTERNAL"
        self.coreVersion = "0.9.0.0"

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k, v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))
