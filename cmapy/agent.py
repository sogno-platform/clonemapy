import cmapy.schemas as schemas

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

    def new_log(logtype, msg, data):
        log = schemas.LogMessage()
        log.logtype = logtype
        log.message = msg
        log.add_data = data
        self.log_out.put(log)