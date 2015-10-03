import thread
from Queue import *

class pong(object):
    def __init__(self):
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
    
    def run(self):
        while 1:
            recv=self.queue_in.get()
            try:
                _, msg_header, msg_payload = recv.split(":",2)
                identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                sender=identification.split("!")
                
                if msg_payload[0]=="\x01" and msg_payload[1:6]=="PING ":
                    self.queue_out.put("NOTICE %s :%s\n"%(sender[0],msg_payload))
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def cmd(self,msg):
        self.queue_in.put(msg)
