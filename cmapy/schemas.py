import json
from datetime import datetime

class LogConfig():
    def __init__(self):
        super().__init__()
        self.msg = False
        self.app = False
        self.status = False
        self.debug = False

    def to_json_dict(self):
        js_dict = {'msg': self.msg, 'app': self.app, 'status': self.status, 'debug': self.debug}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.msg = js_dict.get("msg", False)
        self.app = js_dict.get("app", False)
        self.status = js_dict.get("status", False)
        self.debug = js_dict.get("debug", False)

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class Status():
    def __init__(self):
        super().__init__()
        self.code = 0
        self.last_update = datetime.now()

    def to_json_dict(self):
        js_dict = {"code": self.code, "lastupdate": self.last_update.strftime("%Y-%m-%dT%H:%M:%SZ")}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.code = js_dict.get("code", 0)
        self.last_update = datetime.strptime(js_dict.get("lastupdate", "0-0-0T0:0:0Z"),
            "%Y-%m-%dT%H:%M:%SZ")

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgencySpec():
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.name = 0
        self.id = 0
        self.logger = LogConfig()
        self.agents = []

    def to_json_dict(self):
        js_dict = {"masid": self.masid, "name": self.name, "id": self.id,
            "log": self.logger.to_json_dict(), "agents": self.agents}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.masid = js_dict.get("masid", 0)
        self.name = js_dict.get("name", "")
        self.id = js_dict.get("id", 0)
        self.logger.from_json_dict(js_dict.get("log", LogConfig()))
        self.agents = js_dict.get("agents", [])

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgencyInfo():
    def __init__(self):
        super().__init__()
        self.spec = AgencySpec()
        self.status = Status()

    def to_json_dict(self):
        js_dict = {"spec": self.spec.to_json_dict(), "status": self.status.to_json_dict()}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.spec.from_json_dict(js_dict.get("spec", AgencySpec()))
        self.status.from_json_dict(js_dict.get("status", Status()))

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

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

    def to_json_dict(self):
        js_dict = {"masid": self.masid, "agencyid": self.agencyid, "nodeid": self.nodeid,
            "id": self.id, "name": self.name, "type": self.type, "subtype": self.subtype,
            "custom": self.custom}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.masid = js_dict.get("masid", 0)
        self.agencyid = js_dict.get("agencyid", 0)
        self.nodeid = js_dict.get("nodeid", 0)
        self.id = js_dict.get("id", 0)
        self.name = js_dict.get("name", "")
        self.type = js_dict.get("type", "")
        self.subtype = js_dict.get("subtype", "")
        self.custom = js_dict.get("custom", "")

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class Address():
    def __init__(self):
        super().__init__()
        self.agency = ""

    def to_json_dict(self):
        js_dict = {"agency": self.agency}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.agency = js_dict.get("agency", "")

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgentInfo():
    def __init__(self):
        super().__init__()
        self.spec = AgentSpec()
        self.address = Address()
        self.status = Status()

    def to_json_dict(self):
        js_dict = {"spec": self.spec.to_json_dict(), "address": self.address.to_json_dict(),
            "status": self.status.to_json_dict()}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.spec.from_json_dict(js_dict.get("spec", AgentSpec()))
        self.address.from_json_dict(js_dict.get("address", Address()))
        self.status.from_json_dict(js_dict.get("status", Status()))

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgencyConfig():
    def __init__(self):
        super().__init__()
        self.spec = AgencySpec()
        self.agents = []

    def to_json_dict(self):
        js_dict = {"spec": self.spec.to_json_dict()}
        ag_dicts = []
        for i in self.agents:
            ag_dicts.append(i.to_json_dict())
        js_dict["agents"] = ag_dicts
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.spec.from_json_dict(js_dict.get("spec", AgentSpec()))
        ag_dicts = js_dict.get("agents", [])
        for i in ag_dicts:
            ag = AgentInfo()
            ag.from_json_dict(i)
            self.agents.append(ag)

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)