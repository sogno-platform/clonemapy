import os
import socket
import http.server as server
import threading
import multiprocessing
import time
import json
import requests
import queue
import cmapy.schemas as schemas
import cmapy.ams as ams
import cmapy.agent as agent

class AgencyHandler(server.BaseHTTPRequestHandler):
    """
    Handles http requests to the agency
    """
    def do_GET(self):
        """
        handler function for GET requests
        """
        if self.path == "/api/agency":
            self.handle_get_agency()
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
        print(self.path)
        print(self.server.agency.hostname)
        self.send_response(200)

    def handle_get_agency(self):
        pass
    
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
        pass

    def handle_post_msgs(self):
        """
        handler function for post requests to "/api/agency/msgs
        """
        content_len = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_len)
        print(str(body, 'utf-8'))
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
    Handles the http REST API and manages the agents
    """
    def __init__(self, ag_class):
        super().__init__()
        self.info = schemas.AgencyInfo()
        self.ag_class = ag_class
        self.local_agents = {}
        self.msg_out = multiprocessing.Queue(1000)
        self.lock = multiprocessing.Lock()
        self.remote_agents = {}
        self.remote_agencies = {}
        try:
            log_type = os.environ['CLONEMAP_LOG_LEVEL']
            if log_type == "info":
                pass
            elif log_type == "error":
                pass
            else:
                pass
        except KeyError:
            pass 

        temp = socket.gethostname()
        hostname = temp.split("-")
        self.hostname = hostname
        if len(hostname) < 4:
            pass
        self.info.spec.masid = int(hostname[1])
        self.info.spec.id = int(hostname[3])
        self.info.spec.name = temp + ".mas" + hostname[1] + "agencies"

        x = threading.Thread(target=self.listen)
        x.start()
        self.start_agents()
        time.sleep(5)
        self.send_msg()

    def start_agents(self):
        """
        Requests the agent configuration from the ams and starts the agents
        """
        conf = ams.get_agency_config(self.info.spec.masid, self.info.spec.id)
        self.info.spec.logger = conf.spec.logger
        for i in conf.agents:
            self.create_agent(i)
    
    def create_agent(self, agentinfo):
        """
        execute agent in seperate process
        """
        ag_handler = AgentHandler()
        p = multiprocessing.Process(target=self.ag_class, args=(agentinfo, ag_handler.msg_in, self.msg_out,))
        p.start()
        ag_handler.proc = p
        self.lock.acquire()
        self.local_agents[agentinfo.spec.id] = ag_handler
        self.lock.release()

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
            print(recv)
            self.lock.acquire()
            local_agent = self.local_agents.get(recv, None)
            recv_agency = self.remote_agents.get(recv, None)
            self.lock.release()
            if local_agent != None:
                local_agent.msg_in.put(msg)
                print("Put msg to local agent")
                continue
            elif recv_agency == None:
                self.lock.acquire()
                masid = self.info.spec.masid
                self.lock.release()
                addr = ams.get_agent_address(masid, recv)
                self.lock.acquire()
                agency = self.remote_agencies.get(addr.agency, None)
                self.lock.release()
                if agency == None:
                    agency = queue.Queue(1000)
                    self.lock.acquire()
                    self.remote_agencies[addr.agency] = agency
                    self.lock.release()
                    y = threading.Thread(target=remote_agency_sender, args=(addr.agency, agency,), daemon=True)
                    y.start()
                self.lock.acquire()
                self.remote_agents[recv] = agency
                self.lock.release()
                recv_agency = agency
            recv_agency.put(msg)
            print("Put msg to remote agent")
            # msg_dict = msg.to_json_dict()
            # msg_dicts = []
            # msg_dicts.append(msg_dict)
            # js = json.dumps(msg_dicts)
            # resp = requests.post("http://"+recv_agency+":10000/api/agency/msgs", data=js)

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
        print(address)
        print(js)
        resp = requests.post("http://"+address+":10000/api/agency/msgs", data=js)
        print("sent msg")

if __name__ == "__main__":
    ag = Agency(agent.Agent)
    # time.sleep(5)
    # print("Still here")
    # log = schemas.LogConfig()
    # print(log.to_json())
    # js = log.to_json()
    # log.from_json(js)
    # status = schemas.Status()
    # print(status.to_json())
    # ag_spec = schemas.AgencyConfig()
    # ag_spec.agents.append(schemas.AgentInfo())
    # ag_spec.agents.append(schemas.AgentInfo())
    # print(ag_spec.to_json())