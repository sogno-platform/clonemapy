from datetime import datetime
import cmapy.schemas as schemas
import cmapy.df as df

class Agent():
    """
    super class of agents
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
        log = schemas.LogMessage()
        log.masid = self.masid
        log.agentid = self.id
        log.logtype = logtype
        log.message = msg
        log.add_data = data
        self.log_out.put(log)
        print("put log")

    def register_service(self, svc):
        if svc.desc == "":
            return
        temp = self.registered_svcs.get(svc.desc, None)
        if temp != None:
            return
        svc.created = datetime.now()
        svc.changed = datetime.now()
        svc = df.post_svc(self.masid, svc)
        self.registered_svcs[svc.desc] = svc
        return svc.id

    def search_for_service(self, desc):
        temp = df.get_svc(self.masid, desc)
        svcs = []
        for i in temp:
            if i.agentid != self.id:
                svcs.append(i)
        return svcs

    def search_for_local_service(self, desc, dist):
        temp = df.get_local_svc(self.masid, desc, self.nodeid, dist)
        svcs = []
        for i in temp:
            if i.agentid != self.id:
                svcs.append(i)
        return svcs

    def deregister_service(self, svcid):
        desc = ""
        for temp in self.registered_svcs:
            if self.registered_svcs[temp].id == svcid:
                desc = temp
                break
        if desc == "":
            return
        del self.registered_svcs[desc]
        df.delete_svc(self.masid, svcid)