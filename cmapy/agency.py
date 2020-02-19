import os
import socket
import http.server as server
import threading
import time
import cmapy.schemas as schemas
import cmapy.ams as ams

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
        pass

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

class Agency:
    def __init__(self):
        super().__init__()
        self.info = schemas.AgencyInfo()
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
        print(hostname)
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
    
    def create_agent(self, agent):
        print("Creating agent "+ str(agent.spec.id))

    def listen(self):
        serv = server.HTTPServer
        self.httpd = serv(('', 1111), AgencyHandler)
        self.httpd.agency = self
        self.httpd.serve_forever()

if __name__ == "__main__":
    ag = Agency()
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