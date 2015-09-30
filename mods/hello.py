import threading

#tmp:
import time

class hello(object):
    

    def __init__(self):
        print "created hello"
        self.condition = threading.Event()
        print "created hello"
        #self.condition.acquire()
        print "created hello"
        self.queue=[]
    
    def run(self,some_queue):
        while 1:
            print self.queue
            if len(self.queue)==0:
                print "cleared"
                self.condition.clear()
            self.condition.wait()
            cmd=self.queue.pop(0)
            print "queuemsg:",cmd  # do something with it here
            some_queue.append(cmd)
            
            
    def strr(self):
        print "waiting"
        self.condition.wait()
        print "go"
        
    def cmd(self,msg):
        print "notify"
        self.queue.append(msg)
        self.condition.set()
        print "go2"
