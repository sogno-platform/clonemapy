import os
import socket
import http.server as server
import threading
import time

class AgencyHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
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
        print(self.path)
        print(self.server.agency.hostname)
        self.send_response(200)
    def do_POST(self):
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

class Agency:
    def __init__(self):
        super().__init__()
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
        x = threading.Thread(target=self.listen)
        x.start()

    def listen(self):
        serv = server.HTTPServer
        self.httpd = serv(('', 1111), AgencyHandler)
        self.httpd.agency = self
        self.httpd.serve_forever()

if __name__ == "__main__":
    ag = Agency()
    time.sleep(5)
    print("Still here")