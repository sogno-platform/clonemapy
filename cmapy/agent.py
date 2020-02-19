class Agent():
    def __init__(self, info, msg_in):
        super().__init__()
        self.id = info.spec.id
        self.nodeid = info.spec.nodeid
        self.name = info.spec.name
        self.type = info.spec.type
        self.subtype = info.spec.subtype
        self.custom = info.spec.custom
        self.masid = info.spec.masid
        self.msg_in = msg_in

    def task(self):
        print("This is agent "+ str(self.id))
