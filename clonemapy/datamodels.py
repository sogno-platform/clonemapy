# generated by datamodel-codegen:
#   filename:  openapi.yaml
#   timestamp: 2021-03-02T20:49:04+00:00

from typing import List, Optional

from pydantic import BaseModel, Field

from datetime import datetime

from enum import Enum


class CloneMAP(BaseModel):
    version: Optional[str] = Field(None, description='version of clonemap')
    uptime: Optional[datetime] = Field(None, description='uptime of clonemap')


class ImageGroupConfig(BaseModel):
    image: str = Field(..., description='name of the docker image')
    secret: str = Field(..., description='pull secret to be used for image')


class LoggerConfig(BaseModel):
    active: bool = Field(
        False, description='indicates if logger module is active and/or usable'
    )
    msg: Optional[bool] = Field(None, description='activation of msg log topic')
    app: Optional[bool] = Field(None, description='activation of app log topic')
    status: Optional[bool] = Field(None, description='activation of status log topic')
    debug: Optional[bool] = Field(None, description='activation of debug log topic')


class DFConfig(BaseModel):
    active: bool = Field(
        ..., description='indicates if df module is active and/or usable'
    )


class MQTTConfig(BaseModel):
    active: bool = Field(
        ..., description='indicates if mqtt module is active and/or usable'
    )


class Node(BaseModel):
    id: int = Field(..., description='unique ID of node')
    agents: Optional[List[int]] = Field(
        None, description='list of agents attached to node'
    )


class Edge(BaseModel):
    n1: int = Field(..., description='id of node 1')
    n2: int = Field(..., description='id of node 2')
    weight: float = Field(..., description='weight of edge')


class StatusCode(Enum):
    NotCreated = 0
    Starting = 1
    Initializing = 2
    Running = 3
    Error = 4
    Terminated = 5


class Status(BaseModel):
    code: 'StatusCode' = Field(..., description='status code')
    lastupdate: datetime = Field(default_factory=datetime.now, description='time of last update')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


class AgentSpec(BaseModel):
    nodeid: int = Field(..., description='ID of node')
    name: str = Field(..., description='name/description of agent')
    type: Optional[str] = Field(
        None, description='type of agent (application dependent)'
    )
    subtype: Optional[str] = Field(
        None, description='subtype of agent (application dependent)'
    )
    custom: Optional[str] = Field(None, description='custom agent specification')


class Address(BaseModel):
    agency: Optional[str] = Field(None, description='name of the agency')


class MASConfig(BaseModel):
    name: str = Field(..., description='name of MAS')
    agentsperagency: int = Field(..., description='number of agents per agency')
    mqtt: 'MQTTConfig' = Field(..., description='switch for iot module')
    df: 'DFConfig' = Field(..., description='switch for df module')
    logger: 'LoggerConfig' = Field(..., description='configuration of logging module')


class ImageGroupSpec(BaseModel):
    config: 'ImageGroupConfig' = Field(..., description='configuration of image groups')
    agents: List['AgentSpec'] = Field(
        ..., description='spec of all agents in image groups'
    )


class Graph(BaseModel):
    node: List['Node'] = Field(..., description='list of graph nodes')
    edge: List['Edge'] = Field(..., description='list of graph edges')


class AgencyInfo(BaseModel):
    masid: int = Field(..., description='ID of MAS')
    name: str = Field(
        ..., description='name of agency (hostname of pod given by Kubernetes)'
    )
    id: int = Field(..., description='unique ID of agency')
    imid: int = Field(..., description='unique ID of image group')
    logger: 'LoggerConfig' = Field(LoggerConfig(), description='configuration of logging')
    agents: List[int] = Field([], description='list of all agents in agency')
    status: 'Status' = Field(Status(code=StatusCode.Running), description='status of agency')


class AgentInfo(BaseModel):
    spec: 'AgentSpec' = Field(..., description='spec of Agent')
    masid: int = Field(..., description='ID of MAS')
    agencyid: int = Field(..., description='ID of agency')
    imid: int = Field(..., description='unique ID of image group')
    id: int = Field(..., description='unique ID of agent')
    address: 'Address' = Field(..., description='address of agent')
    status: 'Status' = Field(..., description='status of agent')


class MASInfoShort(BaseModel):
    config: 'MASConfig' = Field(..., description='configuration of MAS')
    id: int = Field(..., description='unique ID of MAS')
    numagents: int = Field(..., description='number of agents')
    status: 'Status' = Field(..., description='status of MAS')
    uptime: datetime = Field(..., description='uptime of MAS')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


class MASSpec(BaseModel):
    config: 'MASConfig' = Field(..., description='configuration of MAS')
    imagegroups: List['ImageGroupSpec'] = Field(..., description='image groups in MAS')
    graph: 'Graph' = Field(..., description='graph of MAS')


class AgencyInfoFull(BaseModel):
    masid: int = Field(..., description='ID of MAS')
    id: int = Field(..., description='ID of agency')
    name: str = Field(..., description='name of agency (corresponds to pod name)')
    imid: int = Field(..., description='id of image group')
    logger: 'LoggerConfig' = Field(LoggerConfig(), description='configuration of logging module')
    status: 'Status' = Field(Status(code=StatusCode.Running), description='status of agent')
    agents: List['AgentInfo'] = Field([], description='list of agents in agency')


class Agents(BaseModel):
    counter: int = Field(..., description='number of running agents')
    instances: List['AgentInfo'] = Field(..., description='all agents in mas')


class Agencies(BaseModel):
    counter: int = Field(..., description='number of running agencies')
    instances: List['AgencyInfo'] = Field(..., description='agencies')


class ImageGroupInfo(BaseModel):
    config: Optional['ImageGroupConfig'] = Field(
        None, description='configuration of image groups'
    )
    id: Optional[int] = Field(None, description='unique id of image groups')
    agencies: Optional['Agencies'] = Field(
        None, description='agencies within image groups'
    )


class ImageGroups(BaseModel):
    counter: int = Field(..., description='number of image groups')
    instances: List['ImageGroupInfo'] = Field(..., description='image groups')


class MASInfo(BaseModel):
    config: 'MASConfig' = Field(..., description='configuration of MAS')
    id: int = Field(..., description='unique ID of MAS')
    graph: 'Graph' = Field(..., description='graph of MAS')
    imagegroups: 'ImageGroups' = Field(..., description='image groups of MAS')
    agents: 'Agents' = Field(..., description='spec of agents')
    status: 'Status' = Field(..., description='status of MAS')
    uptime: datetime = Field(..., description='uptime of MAS')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


class MASs(BaseModel):
    counter: int = Field(..., description='number of running mas')
    instances: List['MASInfo'] = Field(..., description='all mas running in clonemap')


class FipaPerformative(Enum):
    PNone = 0
    AcceptProposal = 1
    Agree = 2
    Cancel = 3
    CallForProposal = 4
    Confirm = 5
    Disconfirm = 6
    Failure = 7
    Inform = 8
    InformIf = 9
    InformRef = 10
    NotUnderstood = 11
    Propagate = 12
    Propose = 13
    Proxy = 14
    QueryIf = 15
    QueryRef = 16
    Refuse = 17
    RejectProposal = 18
    Request = 19
    RequestWhen = 20
    RequestWhenever = 21
    Subscribe = 22


class FipaProtocol(Enum):
    PNone = 0
    Request = 1
    Query = 2
    RequestWhen = 3
    ContractNet = 4
    IteratedContractNet = 5
    EnglishAuction = 6
    DutchAuction = 7
    Brokering = 8
    Recruiting = 9
    Subscribe = 10
    Propose = 11


class ACLMessage(BaseModel):
    ts: datetime = Field(default_factory=datetime.now, description='sending time')
    perf: int = Field(
        0, description='Denotes the type of the communicative act of the ACL message'
    )
    sender: int = Field(
        0, description='Denotes the identity of the sender of the message'
    )
    agencys: str = Field("", description='Denotes the name of the sender agency')
    receiver: int = Field(
        ...,
        description='Denotes the identity of the intended recipients of the message',
    )
    agencyr: str = Field("", description='Denotes the name of the receiver agency')
    repto: Optional[int] = Field(
        None,
        description='This parameter indicates that subsequent messages in this conversation ' +
        'thread are to be directed to the agent named in the reply-to parameter, instead of to ' +
        'the agent named in the sender parameter',
    )
    content: str = Field(..., description='Denotes the content of the message')
    lang: Optional[str] = Field(
        None,
        description='Denotes the language in which the content parameter is expressed',
    )
    enc: Optional[str] = Field(
        None,
        description='Denotes the specific encoding of the content language expression',
    )
    ont: Optional[str] = Field(
        None,
        description='Denotes the ontology(s) used to give a meaning to the symbols in the ' +
        'content expression',
    )
    prot: int = Field(
        0,
        description='Denotes the interaction protocol that the sending agent is employing with ' +
        'this ACL message',
    )
    convid: Optional[int] = Field(
        None,
        description='Introduces an expression which is used to identify the ongoing sequence of ' +
        'communicative acts that together form a conversation',
    )
    repwith: Optional[str] = Field(
        None,
        description='Introduces an expression that will be used by the responding agent to ' +
        'identify this message',
    )
    inrepto: Optional[str] = Field(
        None,
        description='Denotes an expression that references an earlier action to which this ' +
        'message is a reply',
    )
    repby: Optional[str] = Field(
        None,
        description='Denotes a time and/or date expression which indicates the latest time by ' +
        'which the sending agent would like to receive a reply',
    )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }

    def __str__(self):
        ret = "Sender: " + str(self.sender) + ";Receiver: " + str(self.receiver) + ";Timestamp: "
        ret += str(self.ts) + ";Protocol: "
        try:
            ret += FipaProtocol(self.prot).name
        except ValueError:
            ret += "Unknown(" + str(self.prot) + ")"
        ret += ";Performative: "
        try:
            ret += FipaPerformative(self.perf).name
        except ValueError:
            ret += "Unknown(" + str(self.perf) + ")"
        ret += ";Content: " + self.content
        return ret


class LogMessage(BaseModel):
    masid: int = Field(..., description='ID of MAS')
    agentid: int = Field(..., description='ID of Agent')
    topic: str = Field(..., description='type of logging')
    timestamp: datetime = Field(default_factory=datetime.now,
                                description='time at which message was generated')
    msg: str = Field(..., description='message to be logged')
    data: Optional[str] = Field(None, description='additional data')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


class TimeSeriesData(BaseModel):
    masid: int = Field(..., description='ID of MAS')
    agentid: int = Field(..., description='ID of Agent')
    name: str = Field(..., description='name of timeseries')
    timestamp: datetime = Field(default_factory=datetime.now,
                                description='time at which sample was generated')
    value: float = Field(..., description='sample value')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


class State(BaseModel):
    masid: int = Field(..., description='ID of MAS')
    agentid: int = Field(..., description='ID of agent')
    timestamp: datetime = Field(..., description='latest update time')
    state: str = Field(..., description='state of agent')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


class Communication(BaseModel):
    id: int = Field(..., description='id of other agent')
    numsent: int = Field(..., description='number of messages sent to this agent')
    numrecv: int = Field(..., description='number of messages recived from this agent')


class Service(BaseModel):
    id: str = Field("", description='id of service')
    agentid: int = Field(0, description='id of agent which registered service')
    nodeid: int = Field(0, description='id of node')
    masid: int = Field(0, description='id of MAS')
    createdat: datetime = Field(default_factory=datetime.now, description='time of creation')
    changedat: datetime = Field(default_factory=datetime.now, description='time of last change')
    desc: str = Field(..., description='description of service')
    dist: float = Field(0, description='distance')

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat("T") + "Z",
        }


if __name__ == "__main__":
    msg = ACLMessage(perf=0, sender=0, agencys="s", receiver=1, agencyr="r",
                     content="test", prot=10)
    print(msg)
    js = msg.json()
    print(js)
    msg2 = ACLMessage.parse_raw(js, encoding='utf8')
    tem = str(msg2)
    print(tem)
