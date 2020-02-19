import os
import socket
import http.server as server
import threading
import multiprocessing
import time
import json
import cmapy.schemas as schemas
import cmapy.ams as ams
import cmapy.agent as agent

class AgencyHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
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
        if self.path == "/api/agency":
            pass
        elif self.path == "/api/agency/agents":
            self.handle_post_agent()
        elif self.path == "/api/agency/msgs":
            self.handle_post_msgs()
        elif self.path == "/api/agency/msgundeliv":
            self.handle_post_uneliv_msg()
        elif self.path == "/api/agency/agents":
            pass
        else:
            pass

    def handle_post_agent(self):
        pass

    def handle_post_msgs(self):
        content_len = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_len)
        msg_dicts = json.loads(body)
        msgs = []
        for i in msg_dicts:
            msg = schemas.ACLMessage()
            msg.from_json_dict(i)
            msgs.append(msg)

    def handle_post_uneliv_msg(self):
        pass

    def do_DELETE(self):
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
    def __init__(self):
        super().__init__()
        self.msg_in = multiprocessing.Queue(100)

class Agency:
    def __init__(self, ag_class):
        super().__init__()
        self.info = schemas.AgencyInfo()
        self.ag_class = ag_class
        self.agent_handler = {}
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

    def start_agents(self):
        conf = ams.get_agency_config(self.info.spec.masid, self.info.spec.id)
        self.info.spec.logger = conf.spec.logger
        for i in conf.agents:
            self.create_agent(i)
    
    def create_agent(self, agentinfo):
        ag_handler = AgentHandler()
        ag = self.ag_class(agentinfo, ag_handler.msg_in)
        p = multiprocessing.Process(target=ag.task)
        p.start()
        ag_handler.proc = p
        self.agent_handler[agentinfo.spec.id] = ag_handler

    def listen(self):
        serv = server.HTTPServer
        self.httpd = serv(('', 10000), AgencyHandler)
        self.httpd.agency = self
        self.httpd.serve_forever()

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