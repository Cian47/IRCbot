#essential
import thread
from Queue import *

#mods get a tuple:
#(sender, msg_payload, msg_type, msg_receiver)


#for mod
import urllib2
import HTMLParser
import re

days=["week", "monday", "tuesday", "wednesday", "thursday", "friday"]

class mensa(object):
    def __init__(self):
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
        self.h=HTMLParser.HTMLParser()
    
    def run(self):
        while 1:
            cmd=self.queue_in.get()
            if cmd[1][0]=="!" and cmd[1][1:]=="mensa" and cmd[3][0]=="#":
                link="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa"
                content=urllib2.urlopen(link).read().strip('\n\r')
                app=content.split('<td class="ext_sits_speiseplan_rechts"><span class="ext_sits_essen">')
                if len(app)>1:
                    for i in range(1,len(app)):
                        if len(app[i].split("<strong>")[1].split("</strong>")[0]):
                            mens=self.h.unescape(app[i].split("<strong>")[1].split("</strong>")[0])
                            mens=''.join(mens.encode('utf-8'))
                            print mens
                            self.queue_out.put("PRIVMSG "+ cmd[3] +" :"+str(re.sub("\(.*\)","",mens))+"\n")
                            
            elif cmd[1][0]=="!" and cmd[1][1:len("mensa")+1]=="mensa" and cmd[3][0]=="#":
                day = cmd[1].split(" ")[1].lower()
                if day in days:
                    push = 0
                    day_index = days.index(cmd[1].split(" ")[1].lower())
                    if cmd[1].split(" ")[1].lower()=="week":
                        push = 1
                        day_index = 7
                    link="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa&push=%d&day=%d"%(push,day_index)
                    content=urllib2.urlopen(link).read().strip('\n\r')
                    app=content.split('<td class="ext_sits_speiseplan_rechts"><span class="ext_sits_essen">')
                    if len(app)>1:
                        for i in range(1,len(app)):
                            if len(app[i].split("<strong>")[1].split("</strong>")[0]):
                                mens=self.h.unescape(app[i].split("<strong>")[1].split("</strong>")[0])
                                mens=''.join(mens.encode('utf-8'))
                                print mens
                                self.queue_out.put("PRIVMSG "+ cmd[3] +" :"+str(re.sub("\(.*\)","",mens))+"\n")

    def cmd(self,msg):
        self.queue_in.put(msg)
