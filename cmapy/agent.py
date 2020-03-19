"""
This module implements the base class Agent which is to be used for the agent behavior implementation
"""

from datetime import datetime
import cmapy.schemas as schemas
import cmapy.df as df
import cmapy.iot as iot

class Agent():
    """
    Super class of agents

    Agent provides functins for messaging, logging, MQTT and interaction with the DF

    Attributes
    ----------
    id : integer
         unique ID of agent
    nodeid : integer
             ID of node agent is connected to
    name : string
           name of agent
    type : string
           type of agent
    subtype : string
              subtype of agent
    custom : string
             custom agent configuration
    masid : integer
            ID of MAS agent is located in
    registered_svcs : dictionary of schemas.Service
                      all services that have been registered with DF by agent
    msg_in : multiprocessing.Queue
             queue for incoming messages of agent
    msg_out : multiprocessing.Queue
              queue of outgoing messages of agent
    log_out : multiprocessing.Queue
              queue for log messages of agent
    mqtt_client : paho.mqtt.client.Client
                  mqtt client
    """
    def __init__(self, info, msg_in, msg_out, log_out):
        super().__init__()
        self.id = info.spec.id
        self.nodeid = info.spec.nodeid
        self.name = info.spec.name
        self.type = info.spec.type
        self.subtype = info.spec.subtype
        self.custom = info.spec.custom
        self.masid = info.spec.masid
        self.registered_svcs = {}
        self.msg_in = msg_in
        self.msg_out = msg_out
        self.log_out = log_out
        self.mqtt_client = iot.mqtt_connect()
        self.task()

    def task(self):
        """
        test behavior
        """
        print("This is agent "+ str(self.id))
        msg = schemas.ACLMessage()
        msg.content = "Message from agent "+ str(self.id)
        msg.receiver = (self.id+1)%2
        self.send_msg(msg)
        msg = self.recv_msg()
        print(msg.content)
        self.new_log("app", "Test log", "test data")
        svc = schemas.Service()
        svc.desc = "testsvc"
        id = self.register_service(svc)
        print(id)
        temp = self.search_for_service("testsvc")
        for i in temp:
            print(i.desc)
        self.mqtt_subscribe("testtopic")
        self.mqtt_publish("testtopic", "testpayload"+str(self.id))
        msg = self.mqtt_recv_msg()
        print(msg.payload)
        msg = self.mqtt_recv_msg()
        print(msg.payload)

    def recv_msg(self):
        """
        reads one message from incoming message queue; blocks if empty
        """
        msg = self.msg_in.get()
        return msg

    def send_msg(self, msg):
        """
        sends message to receiver
        """
        msg.sender = self.id
        self.msg_out.put(msg)
        print("put msg")

    def new_log(self, logtype, msg, data):
        """
        stores one log messages
        """
        log = schemas.LogMessage()
        log.masid = self.masid
        log.agentid = self.id
        log.logtype = logtype
        log.message = msg
        log.add_data = data
        self.log_out.put(log)
        print("put log")

    def register_service(self, svc):
        """
        registers one service with the DF if service has not been registered before; returns svc ID
        """
        if svc.desc == "":
            return
        temp = self.registered_svcs.get(svc.desc, None)
        if temp != None:
            return
        svc.created = datetime.now()
        svc.changed = datetime.now()
        svc.masid = self.masid
        svc.agentid = self.id
        svc.nodeid = self.nodeid
        svc = df.post_svc(self.masid, svc)
        self.registered_svcs[svc.desc] = svc
        return svc.id

    def search_for_service(self, desc):
        """
        searches for a service and returns all matching services within MAS
        """
        temp = df.get_svc(self.masid, desc)
        svcs = []
        for i in temp:
            if i.agentid != self.id:
                svcs.append(i)
        return svcs

    def search_for_local_service(self, desc, dist):
        """
        searches for a service and returns all matching services within specified distance
        """
        temp = df.get_local_svc(self.masid, desc, self.nodeid, dist)
        svcs = []
        for i in temp:
            if i.agentid != self.id:
                svcs.append(i)
        return svcs

    def deregister_service(self, svcid):
        """
        deregisters the service with svcid
        """
        desc = ""
        for temp in self.registered_svcs:
            if self.registered_svcs[temp].id == svcid:
                desc = temp
                break
        if desc == "":
            return
        del self.registered_svcs[desc]
        df.delete_svc(self.masid, svcid)

    def mqtt_subscribe(self, topic):
        """
        subscribe to a mqtt topic
        """
        self.mqtt_client.subscribe(topic)

    def mqtt_publish(self, topic, payload=None, qos=0, retain=False):
        """
        publishes a mqtt message to a topic
        """
        self.mqtt_client.publish(topic, payload, qos, retain)

    def mqtt_recv_msg(self):
        """
        reads one message from incoming message queue; blocks if empty
        """
        msg = self.mqtt_client.msg_in_queue.get()
        return msg