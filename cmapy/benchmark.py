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
This module implements the agent class for the pingpong benchmark
"""

import json
import time
import paho.mqtt.client as mqtt
import cmapy.agent as agent
import cmapy.agency as agency
import cmapy.schemas as schemas


class CustomData():
    def __init__(self):
        self.benchid = 0
        self.peerid = 0
        self.start = False

    def to_json_dict(self):
        js_dict = {'BenchmarkID': self.benchid, 'PeerID': self.peerid, 'Start': self.start}
        return js_dict

    def to_json(self):
        js_dict = self.to_json_dict()
        js_res = json.dumps(js_dict)
        return js_res

    def from_json_dict(self, js_dict):
        self.benchid = js_dict.get("BenchmarkID", 0)
        self.peerid = js_dict.get("PeerID", 0)
        self.start = js_dict.get("Start", False)

    def from_json(self, js):
        js_dict = json.loads(js)
        self.from_json_dict(js_dict)


class Agent(agent.Agent):
    def __init__(self, info, msg_in, msg_out, log_out):
        super().__init__(info, msg_in, msg_out, log_out)
        # self.test()

    def task(self):
        self.logger.new_log("status", "Starting Test Behavior", "")
        b_acl = self.acl.new_behavior(1, {}, self.handle_acl)
        b_acl.start()
        b_mqtt = self.mqtt.new_behavior("testtopic", self.handle_mqtt)
        b_mqtt.start()
        msg = schemas.ACLMessage()
        if self.id == 0:
            msg.receiver = 1
        else:
            msg.receiver = 0
        msg.content = "test"
        msg.protocol = 1
        time.sleep(10)
        self.acl.send_message(msg)
        self.mqtt.subscribe("testtopic")
        self.mqtt.publish("testtopic", "testpayload"+str(self.id))
        self.loop_forever()

    def handle_acl(self, msg: schemas.ACLMessage):
        print(msg.content)
        self.logger.new_log("status", msg.content, "")

    def handle_mqtt(self, msg: mqtt.MQTTMessage):
        print(msg.payload)

    def pingpong(self):
        cust = CustomData()
        cust.from_json(self.custom)
        self.logger.new_log("status", "Starting PingPong Behavior; Peer: "+str(cust.peerid) +
                            ", Start: " + str(cust.start), "")
        time.sleep(40)
        if cust.start:
            rtts = []
            msg = schemas.ACLMessage()
            msg.receiver = cust.peerid
            msg.content = "test msg"
            for i in range(1000):
                msg.receiver = cust.peerid
                self.acl.send_message(msg)
                msg = self.acl.recv_message_wait()
            for i in range(1000):
                msg.receiver = cust.peerid
                tstart = time.perf_counter()
                self.acl.send_message(msg)
                msg = self.acl.recv_message_wait()
                tstop = time.perf_counter()
                rtt = int((tstop - tstart)*1000000)
                rtts.append(rtt)
            max = 0
            min = 1000000
            sum = 0
            avg = 0
            for i in range(1000):
                if max < rtts[i]:
                    max = rtts[i]
                if min > rtts[i]:
                    min = rtts[i]
                sum += rtts[i]
            avg = int(sum/1000)
            js = json.dumps(rtts)
            self.logger.new_log("status", "RTT in µs: min: "+str(min)+", max: "+str(max)+", avg: " +
                                str(avg), js)
            for i in range(1000):
                msg.receiver = cust.peerid
                self.acl.send_message(msg)
                msg = self.acl.recv_message_wait()
        else:
            while True:
                msg = self.acl.recv_message_wait()
                msg.receiver = msg.sender
                self.acl.send_message(msg)


if __name__ == "__main__":
    ag = agency.Agency(Agent)
