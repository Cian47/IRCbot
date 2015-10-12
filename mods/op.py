#essentials
import thread
from Queue import *
import time


class op(object):
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
                _, msg_header = recv.split(":",1)
                print msg_header
                identification, msg_type, msg_receiver, mode, mode_receiver = msg_header.strip(" ").split(" ")
                print identification, msg_type, msg_receiver 
                sender=identification.split("!")
                
                if msg_type=="MODE" and msg_receiver[0]=="#" and mode_receiver=="Abb0t":
                    if mode=="+o":
                        self.queue_out.put("PRIVMSG %s :Thank you %s, I'll remember that! ;)\n"%(msg_receiver, sender[0]))
                    elif mode=="-o":
                        self.queue_out.put("PRIVMSG %s :Why did you do that, %s?\n"%(msg_receiver, sender[0]))
                    elif mode=="+v":
                        self.queue_out.put("PRIVMSG %s :Oh, I feel awesome now. Thanks %s...</ironic>\n"%(msg_receiver, sender[0]))
                    elif mode=="-v":
                        self.queue_out.put("PRIVMSG %s :Yeah, i hate voice rights, too!\n"%(msg_receiver))
                #do sth, like pong:
                #if msg_payload[0]=="\x01" and msg_payload[1:6]=="PING ":
                #    self.queue_out.put("NOTICE %s :%s\n"%(sender[0],msg_payload))
                
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def cmd(self,msg):
        self.queue_in.put(msg)
