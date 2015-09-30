import socket
import thread

#tmp
import time
import threading 

import mods.hello

class IRCbot(object):
                    
    def __init__(self, args):
        self.args=args
        self.server="irc.underworld.no"
        self.port=6667
        self.nick="Abbot"
        self.channel="#birc"
        #self.ircPassword
        #self.SSL=
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.recv()
        #thread.start_new_thread(self.recvThread,())
        
        
    def connect(self):
        self.sock.connect((self.server, self.port))
        if self.args.verbose:
            print "Connecting to %s:%d"%(self.server,self.port)
        self.sock.send("USER "+ self.nick +" "+ self.nick +"_ "+ self.nick +"__ :"+self.nick+"\n") # user authentication
        self.sock.send("NICK "+ self.nick +"\n") # here we actually assign the nick to the bot
        self.joinChannel(self.channel)
        
    def joinChannel(self, chan):
        print "Joining Channel %s"%chan
        self.sock.send("JOIN "+ chan +"\n")
        
    def message(self, to, msg):
        self.sock.send("PRIVMSG "+ to +" :"+msg+"\n")
        
    def messageList(self, to, msgList):
        for l in msgList:
            message(self, to, l)
            
    def pong(self):
        self.sock.send("PONG :pingis\n")  
            
    def recv(self):
        some_queue=[]
        ## module starting here ##
        test_mod = mods.hello.hello()
        thread.start_new_thread(test_mod.run,(some_queue,)) 
        
        while True:
            recv = self.sock.recv(2048).strip('\n\r')
            if len(recv)!=0:
                print "SOME QUEUE:::::::",some_queue
                print "===\nRECV %d\n==="%len(recv)
                
                if recv.split(":")[0]=="PING ":
                    print "pingpong"
                    self.pong()
                elif len(recv)<512: #tmp for now, there are bigger packets at session start...
                    print recv
                    try:
                        _, msg_header, msg_payload = recv.split(":",2)
                        identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                        sender=identification.split("!")
                                         
                        if msg_payload=="!time":
                            test_mod.cmd(str(time.time()))
                            
                            
                        print recv.split(":",2)
                        print msg_header.split(" ") 
                        print "sender: ",sender
                    except IndexError:
                        if self.args.verbose:
                            print "IndexError"
                        pass
                    except ValueError: # no normal channel/private message
                        if self.args.verbose:
                            print "ValueError"
                        pass
            else:
                print "disconnect ???"
                input(" ... ")
                
                
    
