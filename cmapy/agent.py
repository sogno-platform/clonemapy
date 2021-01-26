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
This module implements the base class Agent which is to be used for the agent behavior implementation
"""

import os
from datetime import datetime
import paho.mqtt.client as mqtt
import multiprocessing
import queue
import threading
import cmapy.schemas as schemas
import cmapy.df as df
from typing import Callable, Dict
import time
# from collections.abc import Callable


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
    df_on: bool
           switch for df
    mqtt_on: bool
             switch for mqtt
    """
    def __init__(self, info: schemas.AgentInfo, msg_in: multiprocessing.Queue, msg_out: multiprocessing.Queue, log_out: multiprocessing.Queue):
        super().__init__()
        self.id = info.id
        self.nodeid = info.spec.nodeid
        self.name = info.spec.name
        self.type = info.spec.type
        self.subtype = info.spec.subtype
        self.custom = info.spec.custom
        self.masid = info.masid
        self.acl = ACL(info.id, msg_in, msg_out)
        self.logger = Logger(info.masid, info.id, log_out)
        self.df = DF(info.masid, info.id, info.spec.nodeid)
        self.mqtt = MQTT()
        # self.task()

    def loop_forever(self):
        while True:
            time.sleep(100)

    def task(self):
        """
        test behavior
        """
        print("This is agent "+ str(self.id))
        msg = schemas.ACLMessage()
        msg.content = "Message from agent "+ str(self.id)
        msg.receiver = (self.id+1)%2
        self.acl.send_message(msg)
        msg = self.acl.recv_message_wait()
        print(msg.content)
        self.logger.new_log("app", "Test log", "test data")
        svc = schemas.Service()
        svc.desc = "testsvc"
        id = self.df.register_service(svc)
        print(id)
        temp = self.df.search_for_service("testsvc")
        for i in temp:
            print(i.desc)
        self.mqtt.subscribe("testtopic")
        self.mqtt.publish("testtopic", "testpayload"+str(self.id))
        msg = self.mqtt.recv_msg()
        print(msg.payload)
        msg = self.mqtt.recv_msg()
        print(msg.payload)


class Behavior():
    """
    abstract base class for agent behaviors
    """
    def __init__(self):
        super().__init__()
        pass

    def start(self):
        """
        starts the behavior
        """
        pass

    def stop(self):
        """
        stops the behavior
        """
        pass

    def _task(self):
        """
        behavior task
        """
        pass


class ACL():
    """
    provides functionality for agent messaging

    Attributes
    ----------
    _id : integer
         unique ID of agent
    _msg_in : multiprocessing.Queue
             queue for incoming messages of agent
    _msg_out : multiprocessing.Queue
              queue of outgoing messages of agent
    _msg_in_protocol : dict
        dict mapping protocols to incoming queues which are checked by behaviors
    """
    def __init__(self, agent_id, msg_in, msg_out):
        super().__init__()
        self._id = agent_id
        self._msg_in = msg_in
        self._msg_in_default = queue.Queue(1000)
        self._msg_out = msg_out
        self._msg_in_protocol = {}
        self._lock = threading.Lock()
        x = threading.Thread(target=self._handle_messages)
        x.start()

    def recv_message_wait(self) -> schemas.ACLMessage:
        """
        reads one message from incoming message queue; blocks if empty
        """
        msg = self._msg_in_default.get()

        return msg

    def recv_messages(self) -> list:
        """
        reads all messages from incoming message queue, if any
        """
        msgs = []
        while True:
            try: 
                msg = self._msg_in_default.get(block=False)
                msgs.append(msg)
            except queue.Empty:
                break
        return msgs

    def send_message(self, msg: schemas.ACLMessage):
        """
        sends message to receiver
        """
        msg.sender = self._id
        self._msg_out.put(msg)

    def _handle_messages(self):
        while True:
            msg = self._msg_in.get()
            self._route_message(msg)

    def _route_message(self, msg: schemas.ACLMessage):
        """
        routes the message to the correct protocol queue or to the general queue if no behavior for the protocol is specified
        """
        self._lock.acquire()
        q = self._msg_in_protocol.get(msg.protocol, None)
        self._lock.release()
        if q == None:
            self._msg_in_default.put(msg)
        else:
            q.put(msg)

    def new_behavior(self, protocol: int, handlePerformative: Dict[int, Callable[[schemas.ACLMessage], None]], handleDefault: Callable[[schemas.ACLMessage], None]) -> Behavior:
        """
        creates a new acl behavior
        """
        beh = ACLBehavior(self, protocol, handlePerformative, handleDefault)
        return beh

    def _register_behavior(self, protocol: int) -> queue.Queue:
        q = queue.Queue(1000)
        self._lock.acquire()
        self._msg_in_protocol[protocol] = q
        self._lock.release()
        return q

    def _de_register_behavior(self, protocol: int):
        self._lock.acquire()
        self._msg_in_protocol.pop(protocol, None)
        self._lock.release()


class MQTT():
    """
    provides functions for MQTT

    Attributes
    ----------
    mqtt_client : paho.mqtt.client.Client
                  mqtt client
    mqtt_on: bool
             switch for mqtt
    """
    def __init__(self):
        super().__init__()
        mqtt_on = os.environ['CLONEMAP_MQTT']
        if mqtt_on == "ON":
            self._on = True
            self._connect()
            self._msg_in_default = queue.Queue(1000)
            self._msg_in_topic = {}
        else:
            self._on = False
        self._lock = threading.Lock()

    def subscribe(self, topic: str):
        """
        subscribe to a mqtt topic
        """
        if not self._on:
            return
        self._client.subscribe(topic)

    def publish(self, topic: str, payload: str =None, qos: int =0, retain: bool =False):
        """
        publishes a mqtt message to a topic
        """
        if not self._on:
            return
        self._client.publish(topic, payload, qos, retain)

    def recv_msg(self) -> mqtt.MQTTMessage:
        """
        reads one message from incoming message queue; blocks if empty
        """
        if not self._on:
            return None
        msg = self._msg_in_default.get()
        return msg

    def recv_latest_msg(self) -> mqtt.MQTTMessage:
        """
        reads the latest message from incoming queue and discards all older messages; blocks is queue is empty
        """
        if not self._on:
            return None
        num_msg = self._msg_in_default.qsize()
        if num_msg == 0:
            # queue is empty wait for next message
            msg = self._msg_in_default.get()
        else:
            # discard num-msg-1 messages and return latest message
            for i in range(num_msg-1):
                msg = self._msg_in_default.get()
            msg = self._msg_in_default.get()
        return msg

    def _on_connect(self, client: mqtt.Client, userdata, flags, rc):
        pass

    def _on_message(self, client: mqtt.Client, userdata, msg):
        """
        add received mqtt message to message queue
        """
        self._route_message(msg)

    def _connect(self):
        """
        connect to broker, start listening for messages and return client
        """
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect("mqtt", 1883, 60)
        self._client.loop_start()

    def _disconnect(self):
        """
        disconnect from broker
        """
        self._client.loop_stop()
        self._client.disconnect()

    def _route_message(self, msg: mqtt.MQTTMessage):
        """
        routes the message to the correct protocol queue or to the general queue if no behavior for the protocol is specified
        """
        self._lock.acquire()
        q = self._msg_in_topic.get(msg.topic, None)
        self._lock.release()
        if q == None:
            self._msg_in_default.put(msg)
        else:
            q.put(msg)

    def new_behavior(self, topic: str, handle: Callable[[mqtt.MQTTMessage], None]) -> Behavior:
        """
        creates a new mqtt behavior
        """
        beh = MQTTBehavior(self, topic, handle)
        return beh

    def new_default_behavior(self, handle: Callable[[mqtt.MQTTMessage], None]) -> Behavior:
        """
        creates a new mqtt behavior
        """
        beh = MQTTBehavior(self, "#", handle)
        return beh

    def _register_behavior(self, topic: str) -> queue.Queue:
        if topic == "#":
            q = self._msg_in_default
        else:
            q = queue.Queue(1000)
            self._lock.acquire()
            self._msg_in_topic[topic] = q
            self._lock.release()
        return q

    def _de_register_behavior(self, topic: str):
        self._lock.acquire()
        self._msg_in_topic.pop(topic, None)
        self._lock.release()


class DF():
    """
    provides functions for interaction with the DF

    Attributes
    ----------
    id : integer
         unique ID of agent
    nodeid : integer
             ID of node agent is connected to
    masid : integer
            ID of MAS agent is located in
    registered_svcs : dictionary of schemas.Service
                      all services that have been registered with DF by agent
    df_on: bool
           switch for df
    """
    def __init__(self, masid, agentid, nodeid):
        super().__init__()
        self.id = agentid
        self.nodeid = nodeid
        self.masid = masid
        self.registered_svcs = {}
        df_on = os.environ['CLONEMAP_DF']
        if df_on == "ON":
            self.df_on = True
        else:
            self.df_on = False

    def register_service(self, svc: schemas.Service) -> int:
        """
        registers one service with the DF if service has not been registered before; returns svc ID
        """
        if not self.df_on:
            return -1
        if svc.desc == "":
            return -1
        temp = self.registered_svcs.get(svc.desc, None)
        if temp != None:
            return -1
        svc.created = datetime.now()
        svc.changed = datetime.now()
        svc.masid = self.masid
        svc.agentid = self.id
        svc.nodeid = self.nodeid
        svc = df.post_svc(self.masid, svc)
        self.registered_svcs[svc.desc] = svc
        return svc.id

    def search_for_service(self, desc: str) -> list:
        """
        searches for a service and returns all matching services within MAS
        """
        svcs = []
        if not self.df_on:
            return svcs
        temp = df.get_svc(self.masid, desc)
        for i in temp:
            if i.agentid != self.id:
                svcs.append(i)
        return svcs

    def search_for_local_service(self, desc: str, dist: float) -> list:
        """
        searches for a service and returns all matching services within specified distance
        """
        svcs = []
        if not self.df_on:
            return svcs
        temp = df.get_local_svc(self.masid, desc, self.nodeid, dist)
        for i in temp:
            if i.agentid != self.id:
                svcs.append(i)
        return svcs

    def deregister_service(self, svcid: int):
        """
        deregisters the service with svcid
        """
        if not self.df_on:
            return
        desc = ""
        for temp in self.registered_svcs:
            if self.registered_svcs[temp].id == svcid:
                desc = temp
                break
        if desc == "":
            return
        del self.registered_svcs[desc]
        df.delete_svc(self.masid, svcid)


class Logger():
    """
    provides functions for logging

    Attributes
    ----------
    id : integer
         unique ID of agent
    masid : integer
            ID of MAS agent is located in
    log_out : multiprocessing.Queue
              queue for log messages of agent
    """
    def __init__(self, masid: int, agentid: int, log_out):
        super().__init__()
        self.id = agentid
        self.masid = masid
        self.log_out = log_out

    def new_log(self, logtype: str, msg: str, data: str):
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


class ACLBehavior(Behavior):
    """
    reactive behavior executed when ACL message is received
    """
    def __init__(self, acl: ACL, protocol: int, handlePerformative: Dict[int, Callable[[schemas.ACLMessage], None]], handleDefault: Callable[[schemas.ACLMessage], None]):
        super().__init__
        self.acl = acl
        self.protocol = protocol
        self.handlePerformative = handlePerformative
        self.handleDefault = handleDefault

    def start(self):
        """
        starts the behavior
        """
        self.q = self.acl._register_behavior(self.protocol)
        x = threading.Thread(target=self._task)
        x.start()

    def stop(self):
        """
        stops the behavior
        """
        pass

    def _task(self):
        """
        behavior task
        """
        while True:
            msg = self.q.get()
            self.handleDefault(msg)


class MQTTBehavior(Behavior):
    """
    reactive behavior executed when MQTT message is received
    """
    def __init__(self, mqtt: MQTT, topic: str, handle: Callable[[mqtt.MQTTMessage], None]):
        super().__init__
        self.mqtt = mqtt
        self.topic = topic
        self.handle = handle

    def start(self):
        """
        starts the behavior
        """
        self.q = self.mqtt._register_behavior(self.topic)
        x = threading.Thread(target=self._task)
        x.start()

    def stop(self):
        """
        stops the behavior
        """
        pass

    def _task(self):
        """
        behavior task
        """
        while True:
            msg = self.q.get()
            self.handle(msg)


class PeriodicBehavior(Behavior):
    """
    reactive behavior executed periodically
    """
    def __init__(self):
        super().__init__

    def start(self):
        """
        starts the behavior
        """
        pass

    def stop(self):
        """
        stops the behavior
        """
        pass

    def _task(self):
        """
        behavior task
        """
        pass