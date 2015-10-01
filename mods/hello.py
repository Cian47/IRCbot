import thread
from Queue import *

#tmp:
import time

class hello(object):
    

    def __init__(self):
        print "created hello"
        #self.condition = threading.Event()
        print "created hello"
        #self.condition.acquire()
        print "created hello"
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
    
    def run(self):
        while 1:
            print self.queue_in
            #if self.queue_in.empty():
            #    print "cleared"
            #    self.condition.clear()
            #self.condition.wait()
            cmd=self.queue_in.get()
            print "queuemsg:",cmd  # do something with it here
            if cmd=="!quit":
                #self.queue_out.put("QUIT #testenv <hass :-(>\n")
                self.queue_out.put("PART #birc :hass euch :-(\n")
            #some_queue.append(cmd)
            
            
    def strr(self):
        print "waiting"
        #self.condition.wait()
        print "go"
        
    def cmd(self,msg):
        print "notify"
        self.queue_in.put(msg)
        #self.condition.set()
        print "go2"
