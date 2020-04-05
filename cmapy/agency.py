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
This module implements an agency compliant with the cloneMAP API.

Start the Agency by creating an object of the agency class. It takes the agent class that implements
the agent behavior to be executed as input parameter. The agent class must be derived from Agent in 
the agent module.

The agency starts an http server which serves the cloneMAP agency API. The agency takes care of 
starting each agent wihin a seperate process. Moreover, it manages the messaging among local and 
remote agents.
"""

import os
import socket
import http.server as server
import threading
import multiprocessing
import time
import json
import requests
import queue
import logging
import cmapy.schemas as schemas
import cmapy.ams as ams
import cmapy.agent as agent
import cmapy.logger as logger
import cmapy.benchmark as benchmark

class AgencyHandler(server.BaseHTTPRequestHandler):
    """
    Handles http requests to the agency
    """
    def do_GET(self):
        """
        handler function for GET requests
        """
        ret = ""
        if self.path == "/api/agency":
            ret = self.handle_get_agency()
        elif self.path == "/api/agency/agents":
            pass
        elif self.path == "/api/agency/msgs":
            pass
        elif self.path == "/api/agency/msgundeliv":
            pass
        elif self.path == "/api/agency/agents":
            pass
        else:
            pass
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(ret.encode())

    def handle_get_agency(self):
        """
        handler function for GET request to /api/agency
        """
        self.server.agency.lock.acquire()
        info = self.server.agency.info
        self.server.agency.lock.release()
        ret = info.to_json()
        return ret
    
    def do_POST(self):
        """
        handler function for POST requests
        """
        if self.path == "/api/agency":
            pass
        elif self.path == "/api/agency/agents":
            self.handle_post_agent()
        elif self.path == "/api/agency/msgs":
            self.handle_post_msgs()
            self.send_response(201)
            self.end_headers()
        elif self.path == "/api/agency/msgundeliv":
            self.handle_post_uneliv_msg()
        elif self.path == "/api/agency/agents":
            pass
        else:
            pass

    def handle_post_agent(self):
        """
        handler function for post request to /api/agency/agents
        """
        pass

    def handle_post_msgs(self):
        """
        handler function for post requests to /api/agency/msgs
        """
        content_len = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_len)
        msg_dicts = json.loads(str(body, 'utf-8'))
        msgs = []
        for i in msg_dicts:
            msg = schemas.ACLMessage()
            msg.from_json_dict(i)
            msgs.append(msg)
        for i in msgs:
            self.server.agency.lock.acquire()
            local_agent = self.server.agency.local_agents.get(i.receiver, None)
            self.server.agency.lock.release()
            if local_agent != None:
                local_agent.msg_in.put(i)

    def handle_post_uneliv_msg(self):
        """
        handler function for post request to /api/agency/msgundeliv
        """
        pass

    def do_DELETE(self):
        """
        handler function for DELETE requests
        """
        if self.path == "/api/agency":
            pass
        elif self.path == "/api/agency/agents":
            pass
        elif self.path == "/api/agency/msgs":
            pass
        elif self.path == "/api/agency/msgundeliv":
            pass
        elif self.path == "/api/agency/agents":
            pass
        else:
            pass

    def handle_delete_agent(self):
        """
        handler function for delete request to /api/agency/agents/{agent-id}
        """
        pass

class AgentHandler:
    """
    Contains the queue for incoming messages of local agents
    """
    def __init__(self):
        super().__init__()
        self.msg_in = multiprocessing.Queue(100)

class Agency:
    """
    Handles the http REST API and manages the agents as well as messaging among agents

    Following threads are started
    - one thread for http server
    - one thread for sending of logs
    - one thread for each remote agency for sending of messages

    Following processes are started:
    - one process for each agent

    Attributes
    ----------
    info : schemas.AgencyInfo
           information about the agency (agency name, agent configuration, ...)
    ag_class : class derived from agent.Agent
               implementation of agent behavior; one ag_class object for each agent is created in a 
               seperate process
    local_agents : dictionary of AgentHandler
                   each local agent has a queue for incoming messages; this is stored in its handler
    msg_out : multiprocessing.Queue
              queue for outgoing messages
    log_out : multiprocessing.Queue
              queue for outgoing log messages
    lock : multiprocessing.Lock
           lock to protect variables from concurrent access
    remote_agents : dictionary of queue.Queue
                    stores the outgoing queue of remote (non-local) agents
    remote_agencies : dictionary of queue.Queue
                      stores the outgoing queue of remote agencies (sending to each remote agency is
                      handled in a seperate thread)
    """
    def __init__(self, ag_class):
        super().__init__()
        self.info = schemas.AgencyInfo()
        self.ag_class = ag_class
        self.local_agents = {}
        self.msg_out = multiprocessing.Queue(1000)
        self.log_out = multiprocessing.Queue(1000)
        self.lock = multiprocessing.Lock()
        self.remote_agents = {}
        self.remote_agencies = {}
        try:
            log_type = os.environ['CLONEMAP_LOG_LEVEL']
            if log_type == "info":
                logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s',
                    level=logging.INFO)
            else:
                logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s',
                    level=logging.ERROR)
        except KeyError:
            logging.basicConfig(format='%(asctime)s - [%(levelname)s] - %(message)s',
                level=logging.ERROR)

        temp = socket.gethostname()
        logging.info("Starting agency " + temp)
        hostname = temp.split("-")
        self.hostname = hostname
        if len(hostname) < 4:
            pass
        self.info.masid = int(hostname[1])
        self.info.imagegroupid = int(hostname[3])
        self.info.id = int(hostname[5])
        self.info.name = temp + ".mas" + hostname[1] + "agencies"

        x = threading.Thread(target=self.listen)
        x.start()
        y = threading.Thread(target=logger.send_logs, args=(self.info.masid, self.log_out,))
        y.start()
        self.start_agents()
        time.sleep(5)
        self.send_msg()

    def start_agents(self):
        """
        Requests the agent configuration from the ams and starts the agents
        """
        conf = ams.get_container_agency_info_full(self.info.masid, self.info.imagegroupid, self.info.id)
        self.info.id = conf.id
        self.info.logger = conf.logger
        logging.info("Starting agents")
        for i in conf.agents:
            self.create_agent(i)
    
    def create_agent(self, agentinfo):
        """
        executes agent in seperate process
        """
        ag_handler = AgentHandler()
        p = multiprocessing.Process(target=self.ag_class, args=(agentinfo, ag_handler.msg_in, self.msg_out, self.log_out,))
        p.start()
        ag_handler.proc = p
        self.lock.acquire()
        self.local_agents[agentinfo.id] = ag_handler
        self.lock.release()
        logging.info("Started agent "+str(agentinfo.id))

    def listen(self):
        """
        open http server
        """
        serv = server.HTTPServer
        self.httpd = serv(('', 10000), AgencyHandler)
        self.httpd.agency = self
        self.httpd.serve_forever()

    def send_msg(self):
        """
        send messages from local agents
        """
        while True:
            msg = self.msg_out.get()
            recv = msg.receiver
            self.lock.acquire()
            local_agent = self.local_agents.get(recv, None)
            recv_agency = self.remote_agents.get(recv, None)
            self.lock.release()
            if local_agent != None:
                # agent is local -> add message to its queue
                local_agent.msg_in.put(msg)
                continue
            elif recv_agency == None:
                # agent is non-local, but address of agent is unknown -> request agent address
                self.lock.acquire()
                masid = self.info.masid
                self.lock.release()
                addr = ams.get_agent_address(masid, recv)
                self.lock.acquire()
                # check if agency of remote agent is known
                agency = self.remote_agencies.get(addr.agency, None)
                self.lock.release()
                if agency == None:
                    # remote agency is not known -> create a queue for messages to this agency and
                    # start a sender in a new thread
                    agency = queue.Queue(1000)
                    self.lock.acquire()
                    self.remote_agencies[addr.agency] = agency
                    self.lock.release()
                    y = threading.Thread(target=remote_agency_sender, args=(addr.agency, agency,),
                        daemon=True)
                    y.start()
                self.lock.acquire()
                self.remote_agents[recv] = agency
                self.lock.release()
                recv_agency = agency
            # add message to queue of remote agent
            recv_agency.put(msg)

def remote_agency_sender(address, out):
    """
    sender to remote agency; executed in seperate thread
    """
    while True:
        msg = out.get()
        msg_dict = msg.to_json_dict()
        msg_dicts = []
        msg_dicts.append(msg_dict)
        js = json.dumps(msg_dicts)
        resp = requests.post("http://"+address+":10000/api/agency/msgs", data=js)
        if resp.status_code != 201:
            pass

if __name__ == "__main__":
    ag = Agency(benchmark.Agent)