#essential
import thread
from Queue import *
import time

#mods get a tuple:
#(sender, msg_payload, msg_type, msg_receiver)


class curtime(object):
    
    def __init__(self):
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
        self.resttime=0
        self.lastcmd=0
    
    def run(self):
        while 1:
            recv=self.queue_in.get()
            try:
                _, msg_header, msg_payload = recv.split(":",2)
                identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                sender=identification.split("!")
                
                if msg_payload[0]=="!" and msg_payload[1:]=="time" and msg_receiver[0]=="#":
                    if time.time() - self.lastcmd > self.resttime:
                        self.lastcmd=time.time()
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" :Current time is \x02%s\x0F\n"%(time.strftime("%H:%M:%S")))
                        
                    else:
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" : - I need a total rest of %d seconds - \n"%self.resttime)

                    
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def cmd(self,msg):
        self.queue_in.put(msg)
