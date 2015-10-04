import time


class Channel(object):
    def __init__(self, name):
        self.channel=name
        self.users=[]
        self.chanmode=""
        self.usermode=""
        self.topic=""
        self.lastmsg=time.time()
        pass
