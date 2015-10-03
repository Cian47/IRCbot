import socket
import thread

#mystuff
from channel import *

import time  # schedule msg output
import sys  # read input for ownSend

#FINAL VARIABLES:
TOPIC="332"
USERLIST="353"
EOFNAMES="366"

class IRCbot(object):         
    def __init__(self, args):
        self.args=args
        self.server="irc.underworld.no"
        self.port=6667
        self.nick="Botler"
        self.channels={}
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
        chans=["#bottle123","#bottle3789"]
        for c in chans:
            self.joinChannel(c)
        
    def joinChannel(self, chan):
        if self.args.verbose:
            print "Joining Channel %s"%chan
        self.channels[chan]=Channel(chan)
        print "CREATED CHANNEL OBJECT"
        print self.channels
        self.sock.send("JOIN "+ chan +"\n")
        
    def leaveChannel(self, chan):
        print "Joining Channel %s"%chan
        self.sock.send("LEAVE "+ chan +"\n")
        
    def message(self, to, msg):
        self.sock.send("PRIVMSG "+ to +" :"+msg+"\n")
        
    def messageList(self, to, msgList):
        for l in msgList:
            message(self, to, l)
            
    def pong(self):
        self.sock.send("PONG :pingis\n")  
            
    def recv(self):
        running_mods=[]
        mods=["pong"]
        for m in mods:
            exec "import mods.%s"%m
            ## module starting here ##
            exec "mod=mods.%s.%s()"%(m,m)
            running_mods.append(mod)
            thread.start_new_thread(self.modHandling,(mod,))
            
        #needed threads
        thread.start_new_thread(self.ownSend,())
            
            
        
        while True:
            recv = self.sock.recv(2048).strip('\n\r')
            if len(recv)!=0:
                print "===\nRECV %d\n==="%len(recv)
                
                if recv.split(":")[0]=="PING ":
                    self.pong()
                elif len(recv.split("\n"))==1:  # single msg = single line ;)
                    print recv
                    for mod in running_mods:
                        mod.cmd(recv)
                else:
                    for l in recv.split("\n"):
                        l=l.strip("\r")
                        cols=l.split(":")
                        if len(cols)>1:  # there has to be a ':', otherwise we dont care
                            if cols[0]=="NOTICE AUTH ":
                                pass
                            #print l
                            content=cols[1].split(" ")
                            if content[0]==self.server and len(content)>1:  # it's a server msg and has -more- content
                                msg_type = content[1]
                                if msg_type==TOPIC:
                                    try:
                                        self.channels[content[3]].topic=cols[2]
                                    except KeyError:
                                        print "ERROR. TOPIC OF %s BUT NO CHANNELOBJECT!"%(content[4])
                                    pass
                                elif msg_type==EOFNAMES:
                                    pass
                                elif msg_type==USERLIST:
                                    try:
                                        self.channels[content[4]].users=cols[2].strip(" ").split(" ")
                                    except KeyError:
                                        print "ERROR. USERLIST OF %s BUT NO CHANNELOBJECT!"%(content[4])
                                    pass
                                elif self.args.verbose:
                                    print "UNKOWN MSG_TYPE %s @ %s"%(msg_type,cols)
                            
            else:
                print "disconnect ???"
                input(" ... ")
                
    def modHandling(self,mod):
        sent = 0
        lastsent = time.time()
        while 1:
            send=mod.queue_out.get()
            if time.time()-lastsent>10:
                sent = 0
            print "SENDING: \n=> '%s'"%send
            self.sock.send(send)
            lastsent=time.time()
            sent += 1
            if sent >= 5:
                time.sleep(1)
        
    def ownSend(self):
        while 1:
            print "ENTER MSG NOW:"
            data = sys.stdin.readlines()
            for d in data:
                self.sock.send(d)
        
    
