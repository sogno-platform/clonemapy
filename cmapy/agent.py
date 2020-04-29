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
    df_on: bool
           switch for df
    mqtt_on: bool
             switch for mqtt
    """
    def __init__(self, info, msg_in, msg_out, log_out):
        super().__init__()
        self.id = info.id
        self.nodeid = info.spec.nodeid
        self.name = info.spec.name
        self.type = info.spec.type
        self.subtype = info.spec.subtype
        self.custom = info.spec.custom
        self.masid = info.masid
        self.registered_svcs = {}
        self.msg_in = msg_in
        self.msg_out = msg_out
        self.log_out = log_out
        df_on = os.environ['CLONEMAP_DF']
        if df_on == "ON":
            self.df_on = True
        else:
            self.df_on = False
        mqtt_on = os.environ['CLONEMAP_MQTT']
        if mqtt_on == "ON":
            self.mqtt_on = True
            self.mqtt_client = iot.mqtt_connect()
        else:
            self.mqtt_on = False
        # self.task()

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

    def register_service(self, svc):
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

    def search_for_service(self, desc):
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

    def search_for_local_service(self, desc, dist):
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

    def deregister_service(self, svcid):
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

    def mqtt_subscribe(self, topic):
        """
        subscribe to a mqtt topic
        """
        if not self.mqtt_on:
            return
        self.mqtt_client.subscribe(topic)

    def mqtt_publish(self, topic, payload=None, qos=0, retain=False):
        """
        publishes a mqtt message to a topic
        """
        if not self.mqtt_on:
            return
        self.mqtt_client.publish(topic, payload, qos, retain)

    def mqtt_recv_msg(self):
        """
        reads one message from incoming message queue; blocks if empty
        """
        if not self.mqtt_on:
            return None
        msg = self.mqtt_client.msg_in_queue.get()
        return msg

    def mqtt_recv_latest_msg(self):
        """
        reads the latest message from incoming queue and discards all older messages; blocks is queue is empty
        """
        if not self.mqtt_on:
            return None
        num_msg = self.mqtt_client.msg_in_queue.qsize()
        if num_msg == 0:
            # queue is empty wait for next message
            msg = self.mqtt_client.msg_in_queue.get()
        else:
            # discard num-msg-1 messages and return latest message
            for i in range(num_msg-1):
                msg = self.mqtt_client.msg_in_queue.get()
            msg = self.mqtt_client.msg_in_queue.get()
        return msg