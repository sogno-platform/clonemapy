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
        self.msg = js_dict["msg"]
        self.app = js_dict["app"]
        self.status = js_dict["status"]
        self.debug = js_dict["debug"]

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class Status():
    def __init__(self):
        super().__init__()
        self.code = 0
        self.last_update = datetime.now()

    def to_json_dict(self):
        js_dict = {"code": self.code, "lastupdate": self.last_update.strftime("%Y-%m-%d %H:%M:%S")}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.code = js_dict["code"]
        self.last_update = datetime.strptime(js_dict["lastupdate"], "%Y-%m-%d %H:%M:%S")

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
        self.masid = js_dict["masid"]
        self.name = js_dict["name"]
        self.id = js_dict["id"]
        self.logger.from_json_dict(js_dict["log"])
        self.agents = js_dict["agents"]

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
        self.spec.from_json_dict(js_dict["spec"])
        self.status.from_json_dict(js_dict["status"])

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
        self.masid = js_dict["masid"]
        self.agencyid = js_dict["agencyid"]
        self.nodeid = js_dict["nodeid"]
        self.id = js_dict["id"]
        self.name = js_dict["name"]
        self.type = js_dict["type"]
        self.subtype = js_dict["subtype"]
        self.custom = js_dict["custom"]

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
        self.agency = js_dict["agency"]

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
        self.spec.from_json_dict(js_dict["spec"])
        self.address.from_json_dict(js_dict["address"])
        self.status.from_json_dict(js_dict["status"])

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
        self.spec.from_json_dict(js_dict["spec"])
        ag_dicts = js_dict["agents"]
        for i in ag_dicts:
            ag = AgentInfo()
            ag.from_json_dict(i)
            self.agents.append(ag)

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)