"""
This module implements the agent class for the pingpong benchmark
"""

import json
import time
import cmapy.agent as agent
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
        super().__init__()

    def pingpong(self):
        cust = CustomData()
        cust.from_json(self.custom)
        self.new_log("status", "Starting PingPong Behavior; Peer: "+str(cust.peerid)+", Start: "+
            str(cust.start), "")
        time.sleep(40)
        if cust.start:
            rtts = []
            msg = schemas.ACLMessage()
            msg.receiver = cust.peerid
            msg.content = "test msg"
            for i in range(1000):
                msg.receiver = cust.peerid
                self.send_msg(msg)
                msg = self.recv_msg()
            for i in range(1000):
                msg.receiver = cust.peerid
                tstart = time.perf_counter()
                self.send_msg(msg)
                msg = self.recv_msg()
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
            self.new_log("status", "RTT in µs: min: "+str(min)+", max: "+str(max)+", avg: "+str(avg), js)
            for i in range(1000):
                msg.receiver = cust.peerid
                self.send_msg(msg)
                msg = self.recv_msg()
        else:
            while True:
                msg = self.recv_msg()
                msg.receiver = msg.sender
                self.send_msg(msg)

