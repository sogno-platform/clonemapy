import json
from datetime import datetime

class LogConfig():
    """
    contains configuration of logging service
    """
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
    """
    contains information about an agent's or agency's status
    """
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
        self.last_update = datetime.strptime(js_dict.get("lastupdate", "0000-00-00T00:00:00Z"),
            "%Y-%m-%dT%H:%M:%SZ")

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgencySpec():
    """
    contains information about agency
    """
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
    """
    contains information about agency spec and status
    """
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
    """
    contains information about a agent running in a MAS
    """
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
    """
    holds the address information of an agent
    """
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
    """
    contains information about agent spec, address, communication, mqtt and status
    """
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
    """
    contains information about agency spec and agents
    """
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

class ACLMessage:
    """
    representing agent message
    """
    def __init__(self):
        super().__init__()
        self.timestamp = datetime.now()
        self.performative = 0
        self.sender = 0
        self.agency_sender = ""
        self.receiver = 0
        self.agency_receiver = ""
        self.reply_to = 0
        self.content = ""
        self.language = ""
        self.encoding = ""
        self.ontology = ""
        self.protocol = 0
        self.conversation_id = 0
        self.reply_with = ""
        self.in_reply_to = 0
        self.reply_by = datetime.now()

    def to_json_dict(self):
        js_dict = {"ts": self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"), "perf": self.performative,
            "sender": self.sender, "agencys": self.agency_sender, "receiver": self.receiver,
            "agencyr": self.agency_receiver, "content": self.content, "prot": self.protocol}
        if self.reply_to != 0:
            js_dict["repto"] = self.reply_to
        if self.language != "":
            js_dict["lang"] = self.language
        if self.encoding != "":
            js_dict["enc"] = self.encoding
        if self.ontology != "":
            js_dict["ont"] = self.ontology
        if self.conversation_id != 0:
            js_dict["convid"] = self.conversation_id
        if self.reply_with != "":
            js_dict["repwith"] = self.reply_with
        if self.in_reply_to != 0:
            js_dict["inrepto"] = self.in_reply_to
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.timestamp = datetime.strptime(js_dict.get("ts", "0000-00-00T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        self.performative = js_dict.get("perf", 0)
        self.sender = js_dict.get("sender", 0)
        self.agency_sender = js_dict.get("agencys", "")
        self.receiver = js_dict.get("receiver", 0)
        self.agency_receiver = js_dict.get("agencyr", "")
        self.reply_to = js_dict.get("repto", 0)
        self.content = js_dict.get("content", "")
        self.language = js_dict.get("lang", "")
        self.encoding = js_dict.get("enc", "")
        self.ontology = js_dict.get("ont", "")
        self.protocol = js_dict.get("prot", 0)
        self.conversation_id = js_dict.get("convid", 0)
        self.reply_with = js_dict.get("repwith", "")
        self.in_reply_to = js_dict.get("inrepto", 0)
        self.reply_by = datetime.strptime(js_dict.get("repby", "0001-01-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        
    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)
