#essential
import thread
from Queue import *
import time

#mods get a tuple:
#(sender, msg_payload, msg_type, msg_receiver)


#for mod
import urllib2
import HTMLParser
import re


days=["week", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

class mensa(object):
    
    def __init__(self):
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
        self.h=HTMLParser.HTMLParser()
        self.resttime=5
        self.lastcmd=0
    
    def run(self):
        while 1:
            recv=self.queue_in.get()
            try:
                _, msg_header, msg_payload = recv.split(":",2)
                identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                sender=identification.split("!")
                
                if msg_payload[0]=="!" and msg_payload[1:]=="mensa" and msg_receiver[0]=="#":
                    self.lastcmd=time.time()
                    self.queue_out.put("PRIVMSG "+ msg_receiver +" :Todays menu:\n")
                    link="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa"
                    content=urllib2.urlopen(link).read().strip('\n\r')
                    
                    self.to_out(content,msg_receiver)
                        
                                
                elif msg_payload[0]=="!" and msg_payload[1:len("mensa")+1]=="mensa" and msg_receiver[0]=="#":
                    self.lastcmd=time.time()
                    day = msg_payload.split(" ")[1].lower()
                    if day == "sunday":
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" :sunday? are you serious?!\n")
                    elif day in days:
                        push = 0
                        day_index = days.index(msg_payload.split(" ")[1].lower())
                        if msg_payload.split(" ")[1].lower()=="week":
                            push = 1
                            day_index = 7
                            self.queue_out.put("PRIVMSG "+ msg_receiver +" :===Next weeks menu===\n")
                        else:
                            self.queue_out.put("PRIVMSG "+ msg_receiver +" :%ss menu:\n"%day)
                        link="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa&push=%d&day=%d"%(push,day_index)
                        content=urllib2.urlopen(link).read().strip('\n\r')
                        ddays=content.split('speise-tblhead')
                        if len(ddays)==1:  # only one day
                        
                            self.to_out(content, msg_receiver)
                            
                        else:  # week?
                            for i in range(1,len(ddays)):
                                self.queue_out.put("PRIVMSG "+ msg_receiver +" :%ss menu:\n"%days[i])
                                
                                self.to_out(ddays[i], msg_receiver)
                    
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def to_out(self, content, msg_receiver):
        app=content.split('<td class="ext_sits_speiseplan_rechts"><span class="ext_sits_essen">')
        if len(app)>1:
            for i in range(1,len(app)):
                if len(app[i].split("<strong>")[1].split("</strong>")[0]):
                    mens=self.h.unescape(app[i].split("<strong>")[1].split("</strong>")[0])
                    mens=''.join(mens.encode('utf-8'))
                    #print mens
                    self.queue_out.put("PRIVMSG "+ msg_receiver +" :  - "+str(re.sub("\(.*\)","",mens))+"\n")
        else:
            self.queue_out.put("PRIVMSG "+ msg_receiver +" :Nothing to eat (anymore) ;[\n")

    def cmd(self,msg):
        self.queue_in.put(msg)
