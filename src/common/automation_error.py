class AutomationError(Exception):
    
    def __init__(self, *args):
        super(Exception, self).__init__(*args)

    def __str__(self):
        return "Automation error is occurred: {0}".format(self.args)

    def __repr__(self):
        return "Automation error is occurred: {0}".format(self.__str__())
