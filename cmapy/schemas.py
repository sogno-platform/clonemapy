import json
from datetime import datetime

class LogConfig():
    def __init__(self):
        super().__init__()
        self.msg = False
        self.app = False
        self.status = False
        self.debug = False

    def get_json_dict(self):
        js_dict = {'msg': self.msg, 'app': self.app, 'status': self.status, 'debug': self.debug}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass

class Status():
    def __init__(self):
        super().__init__()
        self.code = 0
        self.last_update = datetime.now()

    def get_json_dict(self):
        js_dict = {"code": self.code, "lastupdate": self.last_update.strftime("%Y-%m-%d %H:%M:%S")}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

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

    def get_json_dict(self):
        js_dict = {"masid": self.masid, "name": self.name, "id": self.id,
            "log": self.logger.get_json_dict(), "agents": self.agents}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass

class AgencyInfo():
    def __init__(self):
        super().__init__()
        self.spec = AgencySpec()
        self.status = Status()

    def get_json_dict(self):
        js_dict = {"spec": self.spec.get_json_dict(), "status": self.status.get_json_dict()}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

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

    def get_json_dict(self):
        js_dict = {"masid": self.masid, "agencyid": self.agencyid, "nodeid": self.nodeid,
            "id": self.id, "name": self.name, "type": self.type, "subtype": self.subtype,
            "custom": self.custom}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass

class Address():
    def __init__(self):
        super().__init__()
        self.agency = ""

    def get_json_dict(self):
        js_dict = {"agency": self.agency}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass

class AgentInfo():
    def __init__(self):
        super().__init__()
        self.spec = AgentSpec()
        self.address = Address()
        self.status = Status()

    def get_json_dict(self):
        js_dict = {"spec": self.spec.get_json_dict(), "address": self.address.get_json_dict(),
            "status": self.status.get_json_dict()}
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass

class AgencyConfig():
    def __init__(self):
        super().__init__()
        self.spec = AgencySpec()
        self.agents = []

    def get_json_dict(self):
        js_dict = {"spec": self.spec.get_json_dict()}
        ag_dicts = []
        for i in self.agents:
            ag_dicts.append(i.get_json_dict())
        js_dict["agents"] = ag_dicts
        return js_dict

    def to_json(self):
        js_dict = self.get_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json(self, js):
        pass