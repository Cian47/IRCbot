import socket
import thread

#tmp
import time

class IRCbot(object):
        
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
            
    def recvThread(self):
        print "..."
        while True:
            print "...2"
            recv = self.sock.recv(2048).strip('\n\r')
            print "===\nRECV\n===\n",recv
            if recv.find("PING :") != -1: # if the server pings us then we've got to respond!
                print "pingpong"
                self.pong()
            
                
                
                
                
    def __init__(self, args):
        self.args=args
        self.server="irc.underworld.no"
        self.port=6667
        self.nick="Cyborg47"
        self.channel="#birc"
        #self.ircPassword
        #self.SSL=
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.recvThread()
        #thread.start_new_thread(self.recvThread,())
        print "started..?"
        
        
