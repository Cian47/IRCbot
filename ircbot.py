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
GREETONJOIN=2

class IRCbot(object):         
    def __init__(self, args):
        self.args=args
        #self.server="irc.underworld.no"
        self.server="efnet.port80.se"
        #self.server="kornbluth.freenode.net"
        self.port=6667
        self.nick="Abb0t"
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
        #chans=["#bottle123","#bottle3789"]
        chans=[]
        for c in chans:
            self.joinChannel(c)
        
    def joinChannel(self, chan):
        if self.args.verbose:
            print "Joining Channel %s"%chan
        self.channels[chan]=Channel(chan)
        #print "CREATED CHANNEL OBJECT"
        #print self.channels
        self.sock.send("JOIN "+ chan +"\n")
        
    def leaveChannel(self, chan):
        if self.args.verbose:
            print "Leaving Channel %s"%chan
        if chan in self.channels: del self.channels[chan]
        self.sock.send("PRIVMSG "+ chan + " :Gotta go mates, have a good time!\n")
        self.sock.send("PART "+ chan +"\n")
        
    def message(self, to, msg):
        self.sock.send("PRIVMSG "+ to +" :"+msg+"\n")
        
    def messageList(self, to, msgList):
        for l in msgList:
            message(self, to, l)
            
    def pong(self):
        self.sock.send("PONG :pingis\n")  
            
    def recv(self):
        running_mods=[]
        mods=["pong","mensa","op","curtime", "topic", "log"]#,"quiz"]
        for m in mods:
            exec "import mods.%s"%m
            ## module starting here ##
            exec "mod=mods.%s.%s()"%(m,m)
            running_mods.append(mod)
            thread.start_new_thread(self.modHandling,(mod,))
            
        #needed threads
        thread.start_new_thread(self.ownSend,())
            
            
        
        while True:
            recv = self.sock.recv(20000).strip('\n\r')
            if len(recv)!=0:
                print "===\nRECV %d\n==="%len(recv)
                if recv.split(":")[0]=="PING ":
                    self.pong()
                elif len(recv.split("\n"))==1:  # single msg = single line ;)
                    print recv
                    
                    #we parse it, might need it #TODO make method for this
                    try:
                        _, msg_header, msg_payload = recv.split(":",2)
                        identification=""
                        msg_type=""
                        if len(msg_header.strip(" ").split(" "))==3:  # normal msg
                            identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                        elif len(msg_header.strip(" ").split(" "))==2:  # join etc of users
                            identification, msg_type = msg_header.strip(" ").split(" ")
                        sender=identification.split("!")
                        
                        # auto op
                        if msg_type == "JOIN":
                            if sender[0].find("kfreeman")>=0 and sender[1].find("kiwi")>=0:
                                self.sock.send("MODE %s +o %s\n"%(msg_payload,sender[0]))
                        
                    except IndexError:
                        print "IndexError"
                        pass
                    except ValueError: # no normal channel/private message
                        print "ValueError"
                        pass
                    
                    #but we give the whole recv to mods, they may parse on their own                        
                    for mod in running_mods:
                        #print "%d - %d > %d\n%d > %d"%(time.time(),mod.lastcmd,mod.resttime,time.time() - mod.lastcmd,mod.resttime)
                        #if time.time() - mod.lastcmd > mod.resttime:
                            mod.cmd(recv)
                        #else:
                        #    mod.queue_out.put("PRIVMSG "+ msg_receiver +" : - I need a total rest of %d seconds - \n"%mod.resttime)
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
                                    if GREETONJOIN:
                                        user_list=[]
                                        op_list=[]
                                        for u in self.channels[content[3]].users:
                                            if u!=self.nick and u[1:]!=self.nick:
                                                user_list.append(u)
                                                if u[0]=="@":
                                                    op_list.append(u)
                                        if len(user_list)>0:
                                            if GREETONJOIN==1:  # greet everyone and ask for op
                                                self.sock.send("PRIVMSG "+ content[3] +" :Hello %s\n"%(', '.join(user_list)))
                                                if len(op_list)>0:
                                                    self.sock.send("PRIVMSG "+ content[3] +" :I like OP rights, please give me some %s O:-)\n"%(', '.join(op_list)))
                                            elif GREETONJOIN==2:  # just say hi
                                                self.sock.send("PRIVMSG "+ content[3] +" :Hello guys ;]\n")#(mods: %s)\n"%(', '.join(mods)))
                                        
                                            
                                            
                                    pass
                                elif msg_type==USERLIST:
                                    try:
                                        self.channels[content[4]].users=cols[2].strip(" ").split(" ")
                                        nameAt=cols[2].strip(" ").find(self.nick)
                                        if nameAt>0:
                                            mode=cols[2][nameAt-1]
                                            print "USERMODE:",mode,"<<"
                                            if mode!=" ":
                                                self.channels[content[4]].usermode=mode
                                    except KeyError:
                                        print "ERROR. USERLIST OF %s BUT NO CHANNELOBJECT!"%(content[4])
                                    pass
                                elif msg_type=="432":  # erroneous nickname;)
                                    print "error in nickname, choose another one!"
                                    input(" ... ") # TODO exit
                                elif msg_type=="MODE": # modechange e.g. oncreate of channel
                                    print content
                                    self.channels[content[2]].chanmode=content[3]
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
                d=d.strip("\n")
                parameters=filter(None,d.split(" "))
                print parameters
                if len(parameters)>0:
                    if parameters[0]=="JOIN":
                        self.joinChannel(parameters[1])
                    elif parameters[0]=="PART":
                        self.leaveChannel(parameters[1])                    
                    else:
                        self.sock.send(d+"\n")
        
    
