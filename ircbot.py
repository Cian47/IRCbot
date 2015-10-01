import socket
import thread

#tmp
import time
import sys

class IRCbot(object):
                    
    def __init__(self, args):
        self.args=args
        self.server="irc.underworld.no"
        self.port=6667
        self.nick="Botler"
        self.channel="#testenv"
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
        mods=["hello","hello"]
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
                    print "pingpong"
                    self.pong()
                elif len(recv)<512: #tmp for now, there are bigger packets at session start...
                    print recv
                    try:
                        _, msg_header, msg_payload = recv.split(":",2)
                        identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                        sender=identification.split("!")
                        
                        for mod in running_mods:
                            mod.cmd(msg_payload)
                            
                            
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
                
    def modHandling(self,mod):
        while 1:
            send=mod.queue_out.get()
            print "SENDING: %s"%send
            self.sock.send(send)
        
    def ownSend(self):
        while 1:
            print "ENTER MSG NOW:"
            data = sys.stdin.readlines()
            for d in data:
                self.sock.send(d)
        
    
