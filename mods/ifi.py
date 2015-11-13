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

class ifi(object):
    
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
                
                if msg_payload[0]=="!" and msg_payload[1:]=="ifi" and msg_receiver[0]=="#":
                    if time.time() - self.lastcmd > self.resttime:
                        self.lastcmd=time.time()
                        
                        link="http://display.informatik.uni-goettingen.de/events.html"
                        content=urllib2.urlopen(link).read().strip('\n\r')
                        
                        self.to_out(content,msg_receiver)
                    else:
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" : - I need a total rest of %d seconds - \n"%self.resttime)
                        
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass

    def to_out(self, content, msg_receiver):
        classes=content.split("<table")[2].split("</table>")[0]
        for j in range(1,len(classes.split("<tr"))):
            to_say=""
            if classes.split("<tr")[j].find("<br")!=-1:
                for i in range(0,4):
                    if i==0:
                        to_say+=" \x02=>\x0F "
                        to_say+="%-13s | "%classes.split("<tr")[j].split("</td>")[i].split("<td")[1].split(">")[1].split("<")[0].replace("<br","").strip("\t\n ")
                    elif i==1:
                        class_say=classes.split("<tr")[j].split("</td>")[i].split("<td")[1].split(">")[1].split("<")[0].replace("<br","").strip("\t\n ")
                        spaces_umlaute=len(class_say)-len(class_say.decode("utf-8"))
                        leng="%d"%(50+spaces_umlaute)
                        leng="%-"+leng+"s | "
                        to_say+=leng%classes.split("<tr")[j].split("</td>")[i].split("<td")[1].split(">")[1].split("<")[0].replace("<br","").strip("\t\n ") #umlaute
                    elif i==2:
                        pass
                        #to_say+="%-6s | "%classes.split("<tr")[j].split("</td>")[i].split("<td")[1].split(">")[1].split("<")[0].replace("<br","").strip("\t\n ")
                    elif i==3:
                        to_say+="%-20s"%classes.split("<tr")[j].split("</td>")[i].split("<td")[1].split(">")[1].split("<")[0].replace("<br","").strip("\t\n ")
            else:
                to_say+="\x02"+classes.split("<tr")[j].split("</td>")[0].split("<td")[1].split(">")[1].split("<")[0].replace("<br","").strip("\t\n ")
            print to_say
            self.queue_out.put("PRIVMSG "+ msg_receiver +" :"+to_say+"\n")

    def cmd(self,msg):
        self.queue_in.put(msg)
