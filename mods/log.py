#essential
import thread
from Queue import *
import time
import gzip

#mods get a tuple:
#(sender, msg_payload, msg_type, msg_receiver)


class log(object):
    
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
                
                if msg_payload and msg_receiver[0]=="#":
                    with gzip.open("msglog.gz","a+") as log:
                        print "logged:",msg_payload
                        log.write(msg_payload+"\n")

                    
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def cmd(self,msg):
        self.queue_in.put(msg)
