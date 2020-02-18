import json

class LogConfig():
    def __init__(self):
        super().__init__()
        self.msg = False
        self.app = False
        self.status = False
        self.debug = False

    def to_json(self):
        js_dict = {'msg': self.msg, 'app': self.app, 'status': self.status, 'debug': self.debug}
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass

class Status():
    def __init__(self):
        super().__init__()
        self.code = 0

    def to_json(self):
        pass

    def from_json(self, js):
        pass

class AgencySpec():
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.name = 0
        self.id = 0
        self.logger = LogConfig()
        self.agents = []

    def to_json(self):
        pass

    def from_json(self, js):
        pass

class AgencyInfo():
    def __init__(self):
        super().__init__()
        self.spec = AgencySpec()
        self.status = Status()

    def to_json(self):
        pass

    def from_json(self, js):
        pass

class AgentSpec():
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.agencyid = 0
        self.nodeid = 0
        self.id = 0
        self.name = ""
        self.type = ""
        self.subtype = ""
        self.custom = ""

    def to_json(self):
        pass

    def from_json(self, js):
        pass

class Address():
    def __init__(self):
        super().__init__()
        self.agency = ""

    def to_json(self):
        pass

    def from_json(self, js):
        pass

class AgentInfo():
    def __init__(self):
        super().__init__()
        self.spec = AgentSpec()
        self.address = Address()
        self.status = Status()

    def to_json(self):
        pass

    def from_json(self, js):
        pass

class AgencyConfig():
    def __init__(self):
        super().__init__()
        self.spec = AgencySpec()
        self.agents = []

    def to_json(self):
        pass

    def from_json(self, js):
        pass