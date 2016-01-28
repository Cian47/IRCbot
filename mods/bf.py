#essentials
import thread
from Queue import *
import time

#for mod
from StringIO import StringIO
import sys,io
import curses.ascii
from pybrainfuck import BrainFck
import signal
#"++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.+++."




class bf(object):
        
    def __init__(self):
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
        self.resttime=0
        self.lastcmd=0
        self.fo=StringIO()
        self.bfck = BrainFck(fout=self.fo)
    
    def run(self):
        while 1:
            recv=self.queue_in.get()
            try:
                _, msg_header, msg_payload = recv.split(":",2)
                identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                sender=identification.split("!")
                
                if msg_payload[0]=="!" and msg_payload[1:3]=="bf" and msg_receiver[0]=="#":
                    inbf=io.BytesIO(msg_payload.split(" ",1)[1])
                    #signal.alarm(2)   #
                    try:
                        print "start"
                        self.bfck.run(inbf)
                        for i,c in enumerate(self.fo.buflist):
                            if not curses.ascii.isprint(c):
                                self.fo.buflist[i]=""
                        outbf="".join(self.fo.buflist).strip("\n\r")
                        self.fo.read()
                    except Exception:
                        outbf="Timed out!"
                    

                    self.queue_out.put("PRIVMSG "+ msg_receiver +" :"+outbf+"\n")
                
            except IndexError:
                pass
            except ValueError: # no normal channel/private message
                pass

    def cmd(self,msg):
        self.queue_in.put(msg)
