# Copyright 2020 Institute for Automation of Complex Power Systems,
# E.ON Energy Research Center, RWTH Aachen University
#
# This project is licensed under either of
# - Apache License, Version 2.0
# - MIT License
# at your option.
#
# Apache License, Version 2.0:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# MIT License:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This module implements the cloneMAP schemas with json marshalling/unmarshalling
"""
import json
from datetime import datetime

class LogConfig():
    """
    contains configuration of logging service

    Attributes
    ----------
    msg : Boolean
        switch for enabling logging to topic msg
    app : Boolean
        switch for enabling logging to topic app
    status : Boolean
        switch for enabling logging to topic status
    debug : Boolean
        switch for enabling logging to topic debug
    """
    def __init__(self):
        super().__init__()
        self.msg = False
        self.app = False
        self.status = False
        self.debug = False

    def to_json_dict(self) -> dict:
        js_dict = {'msg': self.msg, 'app': self.app, 'status': self.status, 'debug': self.debug}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.msg = js_dict.get("msg", False)
        self.app = js_dict.get("app", False)
        self.status = js_dict.get("status", False)
        self.debug = js_dict.get("debug", False)

    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class Status():
    """
    contains information about an agent's or agency's status

    Attributes
    ----------
    code : int
        status code
    last_update : datetime
        time of last status update
    """
    def __init__(self):
        super().__init__()
        self.code = 0
        self.last_update = datetime.now()

    def to_json_dict(self) -> dict:
        js_dict = {"code": self.code, "lastupdate": self.last_update.strftime("%Y-%m-%dT%H:%M:%SZ")}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.code = js_dict.get("code", 0)
        self.last_update = datetime.strptime(js_dict.get("lastupdate", "0000-00-00T00:00:00Z"),
            "%Y-%m-%dT%H:%M:%SZ")

    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgencyInfoFull():
    """
    contains information about agency and agents

    Attributes
    ----------
    masid : int
        ID of the MAS
    name : str
        name of the agency
    id : int
        ID of the agency
    imagegroupid: int
        ID of the image group
    logger: LogConfig
        configuration of the logger
    agents: list(AgentInfo)
        agents in this agency
    status: Status
        status of the agency
    """
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.name = ""
        self.id = 0
        self.imagegroupid = 0
        self.logger = LogConfig()
        self.agents = []
        self.status = Status()

    def to_json_dict(self) -> dict:
        js_dict = {"masid": self.masid, "name": self.name, "id": self.id,
            "imid": self.imagegroupid, "log": self.logger.to_json_dict(),
            "status": self.status.to_json_dict()}
        ag_dicts = []
        for i in self.agents:
            ag_dicts.append(i.to_json_dict())
        js_dict["agents"] = ag_dicts
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.masid = js_dict.get("masid", 0)
        self.name = js_dict.get("name", "")
        self.id = js_dict.get("id", 0)
        self.imagegroupid = js_dict.get("imid", 0)
        self.logger.from_json_dict(js_dict.get("log", LogConfig()))
        self.status = js_dict.get("status", Status())
        ag_dicts = js_dict.get("agents", [])
        for i in ag_dicts:
            ag = AgentInfo()
            ag.from_json_dict(i)
            self.agents.append(ag)


    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgencyInfo():
    """
    contains information agency

    Attributes
    ----------
    masid : int
        ID of the MAS
    name : str
        name of the agency
    id : int
        ID of the agency
    imagegroupid: int
        ID of the image group
    logger: LogConfig
        configuration of the logger
    agents: list(int)
        agents in this agency
    status: Status
        status of the agency
    """
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.name = ""
        self.id = 0
        self.imagegroupid = 0
        self.logger = LogConfig()
        self.agents = []
        self.status = Status()

    def to_json_dict(self) -> dict:
        js_dict = {"masid": self.masid, "name": self.name, "id": self.id,
            "imid": self.imagegroupid, "log": self.logger.to_json_dict(), "agents": self.agents,
            "status": self.status.to_json_dict()}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.masid = js_dict.get("masid", 0)
        self.name = js_dict.get("name", "")
        self.id = js_dict.get("id", 0)
        self.imagegroupid = js_dict.get("imid", 0)
        self.logger.from_json_dict(js_dict.get("log", LogConfig()))
        self.agents = js_dict.get("agents", [])
        self.status = js_dict.get("status", Status())

    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgentSpec():
    """
    contains information about a agent running in a MAS

    Attributes
    ----------
    nodeid : int
        ID of the node the agent is attached to
    name : str
        name of the agent
    type : str
        type of the agent
    subtype : str
        subtype of the agent
    custom : str
        custom configuration of the agent
    """
    def __init__(self):
        super().__init__()
        self.nodeid = 0
        self.name = ""
        self.type = ""
        self.subtype = ""
        self.custom = ""

    def to_json_dict(self) -> dict:
        js_dict = {"nodeid": self.nodeid,
            "name": self.name, "type": self.type, "subtype": self.subtype,
            "custom": self.custom}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.nodeid = js_dict.get("nodeid", 0)
        self.name = js_dict.get("name", "")
        self.type = js_dict.get("type", "")
        self.subtype = js_dict.get("subtype", "")
        self.custom = js_dict.get("custom", "")

    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class Address():
    """
    holds the address information of an agent

    Attributes
    ----------
    agency : str
        agency name
    """
    def __init__(self):
        super().__init__()
        self.agency = ""

    def to_json_dict(self) -> dict:
        js_dict = {"agency": self.agency}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.agency = js_dict.get("agency", "")

    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class AgentInfo():
    """
    contains information about agent spec, address, communication, mqtt and status

    Attributes
    ----------
    spec : AgentSpec
        specs of the agent
    masid : int
        ID of the MAS
    agencyid : int
        ID of the agency
    imagegroupid : int
        IF of the image group
    address : Address
        address of the agent
    status : Status
        status of the agent
    """
    def __init__(self):
        super().__init__()
        self.spec = AgentSpec()
        self.masid = 0
        self.agencyid = 0
        self.imagegroupid = 0
        self.id = 0
        self.address = Address()
        self.status = Status()

    def to_json_dict(self) -> dict:
        js_dict = {"spec": self.spec.to_json_dict(), "masid": self.masid, "agencyid": self.agencyid,
            "imid": self.imagegroupid, "id": self.id, "address": self.address.to_json_dict(),
            "status": self.status.to_json_dict()}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.spec.from_json_dict(js_dict.get("spec", AgentSpec()))
        self.masid = js_dict.get("masid", 0)
        self.name = js_dict.get("agencyid", 0)
        self.id = js_dict.get("id", 0)
        self.imagegroupid = js_dict.get("imid", 0)
        self.address.from_json_dict(js_dict.get("address", Address()))
        self.status.from_json_dict(js_dict.get("status", Status()))

    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class ACLMessage:
    """
    representing agent message

    Attributes
    ----------
    timestamp : datetime
        time when message is sent
    performative : int
        denoting performative act
    sender : int
        ID of the sender
    agency_sender : str
        name of the sender's agency
    receiver : int
        ID of the receiver
    agency_receiver : str
        name of the receiver's agency
    reply_to : int
        ID of agent that should be replied to
    content : str
        content of the message
    language : str
        language of the content
    encoding : str
        encoding of the content
    ontology : str
        ontology of the content
    protocol : int
        protocol of the message
    conversation_id : int
        ID of the conversation
    reply_with : str
        content to reply with
    in_reply_to : int
        ID of message that is replied to
    reply_by : datetime
        time until reply must be sent
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

    def to_json_dict(self) -> dict:
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

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
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
        
    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class LogMessage:
    """
    representing log message

    Attributes
    ----------
    masid : int
        ID of the MAS
    agentid : int
        ID of the agent
    timestamp : datetime
        time at which log message was created
    logtype : str
        topic of the log (app, status, msg, error, debug)
    message : str
        log message
    add_data : str
        additional data
    """
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.agentid = 0
        self.timestamp = datetime.now()
        self.logtype = ""
        self.message = ""
        self.add_data = ""

    def to_json_dict(self) -> dict:
        js_dict = {"masid": self.masid, "agentid": self.agentid, "timestamp": self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "logtype": self.logtype, "msg": self.message}
        if self.add_data != "":
            js_dict["data"] = self.add_data
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.masid = js_dict.get("masid", 0)
        self.agentid = js_dict.get("agentid", 0)
        self.timestamp = datetime.strptime(js_dict.get("timestamp", "0000-00-00T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        self.logtype = js_dict.get("logtype", "")
        self.message = js_dict.get("message", "")
        self.add_data = js_dict.get("data", "")
        
    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class State:
    """
    representing agent state

    Attributes
    ----------
    masid : int
        ID of the MAS
    agentid : int
        ID of the agent
    timestamp : datetime
        time at which state was created
    state : str
        state of agent
    """
    def __init__(self):
        super().__init__()
        self.masid = 0
        self.agentid = 0
        self.timestamp = datetime.now()
        self.state = ""

    def to_json_dict(self) -> dict:
        js_dict = {"masid": self.masid, "agentid": self.agentid, "timestamp": self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "state": self.state}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.masid = js_dict.get("masid", 0)
        self.agentid = js_dict.get("agentid", 0)
        self.timestamp = datetime.strptime(js_dict.get("timestamp", "0000-00-00T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        self.state = js_dict.get("state", "")
        
    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)

class Service:
    """
    representing service

    Attributes
    ----------
    agentid : int
        ID of offering service
    nodeid : int
        ID of node agent is attached to
    masid : int
        ID of MAS
    created : datetime
        time at which service was created
    changed : datetime
        last time at which service was changed
    desc : str
        service description
    dist : float
        distance to own node
    """
    def __init__(self):
        super().__init__()
        self.id = ""
        self.agentid = 0
        self.nodeid = 0
        self.masid = 0
        self.created = datetime.now()
        self.changed = datetime.now()
        self.desc = ""
        self.dist = 0.0

    def to_json_dict(self) -> dict:
        js_dict = {"id": self.id, "agid": self.agentid, "nodeid": self.nodeid, "masid": self.masid,
            "crat": self.created.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "chat": self.changed.strftime("%Y-%m-%dT%H:%M:%SZ"), "desc": self.desc, "dist": self.dist}
        return js_dict

    def to_json(self) -> str:
        js_dict = self.to_json_dict()
        js_res = ""
        try:
            js_res = json.dumps(js_dict)
        except TypeError:
            pass
        return js_res

    def from_json_dict(self, js_dict: dict):
        self.id = js_dict.get("id", "")
        self.agentid = js_dict.get("agid", 0)
        self.nodeid = js_dict.get("nodeid", 0)
        self.masid = js_dict.get("masid", 0)
        self.created = datetime.strptime(js_dict.get("crat", "0000-00-00T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        self.changed = datetime.strptime(js_dict.get("chat", "0000-00-00T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        self.desc = js_dict.get("desc", "")
        self.dist = js_dict.get("dist", 0.0)
        
    def from_json(self, js: str):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)