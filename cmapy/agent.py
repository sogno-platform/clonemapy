import cmapy.schemas as schemas

def agent_starter(ag_class, info, msg_in, msg_out):
    print("Agent starter")
    msg_out.put("45")
    #ag = ag_class(info, msg_in, msg_out)
    #ag.task()

class Agent():
    def __init__(self, info, msg_in, msg_out):
        super().__init__()
        self.id = info.spec.id
        self.nodeid = info.spec.nodeid
        self.name = info.spec.name
        self.type = info.spec.type
        self.subtype = info.spec.subtype
        self.custom = info.spec.custom
        self.masid = info.spec.masid
        self.msg_in = msg_in
        self.msg_out = msg_out
        self.task()

    def task(self):
        print("This is agent "+ str(self.id))
        msg = schemas.ACLMessage()
        msg.content = "Message from agent "+ str(self.id)
        msg.receiver = (self.id+1)%2
        self.send_msg(msg)
        # msg = self.recv_msg()
        # print(msg.content)

    def recv_msg(self):
        msg = self.msg_in.get()
        return msg

    def send_msg(self, msg):
        msg.sender = self.id
        self.msg_out.put(msg)
        print("put msg")