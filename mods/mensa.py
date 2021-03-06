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
        self.resttime=10
        self.lastcmd=0
    
    def run(self):
        while 1:
            recv=self.queue_in.get()
            try:
                _, msg_header, msg_payload = recv.split(":",2)
                identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                sender=identification.split("!")
                
                if msg_payload[0]=="!" and msg_payload[1:]=="mensa" and msg_receiver[0]=="#":
                    if time.time() - self.lastcmd > self.resttime:
                        self.lastcmd=time.time()
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" :\x02\x1FTodays menu:\n")
                        link="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa"
                        content=urllib2.urlopen(link).read().strip('\n\r')
                        
                        self.to_out(content,msg_receiver)
                    else:
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" : - I need a total rest of %d seconds - \n"%self.resttime)
                        
                                
                elif msg_payload[0]=="!" and msg_payload[1:len("mensa")+1]=="mensa" and msg_receiver[0]=="#":
                    if time.time() - self.lastcmd > self.resttime:
                        self.lastcmd=time.time()
                        day = msg_payload.split(" ")[1].lower()
                        if day == "sunday":
                            self.queue_out.put("PRIVMSG "+ msg_receiver +" :\x02\x1Fsunday\x0F? are you serious?!\n")
                        elif day in days:
                            push = 0
                            day_index = days.index(msg_payload.split(" ")[1].lower())
                            if msg_payload.split(" ")[1].lower()=="week":
                                push = 1
                                day_index = 7
                                self.queue_out.put("PRIVMSG "+ sender[0] +" :\x02\x1F===Next weeks menu===\n")
                            else:
                                self.queue_out.put("PRIVMSG "+ msg_receiver +" :\x02\x1F%ss menu:\n"%day)
                            link="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa&push=%d&day=%d"%(push,day_index)
                            content=urllib2.urlopen(link).read().strip('\n\r')
                            ddays=content.split('speise-tblhead')
                            if len(ddays)==1:  # only one day
                            
                                self.to_out(content, msg_receiver)
                                
                            else:  # week?
                                for i in range(1,len(ddays)):
                                    self.queue_out.put("PRIVMSG "+ sender[0] +" :\x02\x1F%ss menu:\n"%days[i])
                                    
                                    self.to_out(ddays[i], sender[0])
                    else:
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" : - I need a total rest of %d seconds - \n"%self.resttime)
                    
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def to_out(self, content, msg_receiver):
        app=content.split('<td class="ext_sits_speiseplan_rechts"><span class="ext_sits_essen">')
        dishes=[]
        fruits=[]
        if len(app)>1:
            for i in range(1,len(app)):
                if len(app[i].split("<strong>")[1].split("</strong>")[0]):
                    mens=self.h.unescape(app[i].split("<strong>")[1].split("</strong>")[0])
                    mens=''.join(mens.encode('utf-8'))
                    #print mens
                    self.queue_out.put("PRIVMSG "+ msg_receiver +" :  - \x02"+str(re.sub("\(.*\)","",mens)).strip(" ")+"\n")
                if len(app[i].split("</strong>")[1].split("</span>")[0].strip("\r\n\t")): #dish
                    dish=self.h.unescape(app[i].split("</strong>")[1].split("</span>")[0].strip("\r\n\t"))
                    dish=''.join(dish.encode('utf-8'))
                    if dish.lower().find("verschiedene salat-")==-1 and dish.lower().find("nur solange der vor")==-1:
                    #self.queue_out.put("PRIVMSG "+ msg_receiver +" :  - \x02"+str(re.sub("\(.*\)","",dish))+"\n")
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" :  ===> "+str(re.sub("\(.*\)","",dish).replace(" ,",",")).strip(" ")+"\n")
                    #if dish.lower().find("sauce")==-1 and dish.lower().find("dressing")==-1:
                    #    dishes.append(dish.split(", ")[:-1])
                    #fruits.append(dish.split(", ")[-1])
            #if len(dishes)>0:
            #    print dishes
            #    dishes_string=[]
            #    for k in range(len(dishes)-2):
            #        for l in range(len(dishes[k])):
            #            if str(re.sub("\(.*\)","",dishes[k][l])).strip(" ") not in dishes_string:
            #                dishes_string.append(str(re.sub("\(.*\)","",dishes[k][l])).strip(" "))
            #    self.queue_out.put("PRIVMSG "+ msg_receiver +" :  - \x02\x1DSide dishes\x0F: "+', '.join(dishes_string)+"\n")
                    
            print dishes    
            print fruits
        else:
            self.queue_out.put("PRIVMSG "+ msg_receiver +" :Nothing to eat (anymore) ;[\n")

    def cmd(self,msg):
        self.queue_in.put(msg)
