# Import some necessary libraries.
import socket 
import thread
import time
import urllib2
import random
import HTMLParser
import sys
import ast
import re

#!date
import datetime
import math

statsfile = open("stats").read()

exp = int(statsfile.split("\n")[0])
userstats = ast.literal_eval(statsfile.split("\n")[1])
print userstats
level = int(math.sqrt(exp))
# Some basic variables used to configure the bot        
server = "irc.underworld.no" # Server       
#server = "irc.freenode.net" # Server
channel = "#birc" # Channel
botnick = "Mensa47" # Your bots nick

h=HTMLParser.HTMLParser()

lst=[("12:20:00","10 Minutes left!"),("12:30:00","GoGoGo MensaTime")]


def ping(): # This is our first function! It will respond to server Pings.
    ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
    ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
    ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello Mybot"
    ircsock.send("PRIVMSG "+ channel +" :Hello!\n")
       

def bullshit():
    while 1:
        now = datetime.datetime.now()
        #print lst
        for i,l in enumerate(lst):
            if l[0]==now.strftime("%H:%M:%S"):
                ircsock.send("PRIVMSG "+ channel +" :"+lst[i][1]+"\n")
                if i>=2:
                    lst.remove(l)
        #if "12:20:00"==
            
        #elif "12:30:00"==now.strftime("%H:%M:%S"):
        #    ircsock.send("PRIVMSG "+ channel +" :GoGoGo MensaTime!\n")
        time.sleep(1)
        
        

def msgs():
    while 1:
        print "ENTER MSG NOW:"
        data = sys.stdin.readlines()
        for d in data:
            ircsock.send("PRIVMSG "+ channel +" :"+d)
            
            

def google():
    var=0
    while 1:
        link="https://plus.google.com/+KevinFreeman47/posts"
        res=urllib2.urlopen(link)
        res=res.read().strip('\n\r')
        w=res.split('herungswerte)">')[1].split("</span>")[0]
        wait=random.randint(10,25)
        print "opened",var,"got:",w,"wait",wait
        var+=1
        time.sleep(wait)
        
   
       
                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +"_ "+ botnick +"__ :HBotter\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined
#thread.start_new_thread(msghandling,())

days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

while 1: # Be careful with these! it might send you to an infinite loop
    with open("stats","w") as fw:
        fw.write(str(exp)+"\n")
        fw.write(str(userstats))
    if int(math.sqrt(exp))!=level:
        level = int(math.sqrt(exp))
        ircsock.send("PRIVMSG "+ channel +" :===========================\n")
        ircsock.send("PRIVMSG "+ channel +" :=  I reached level %4s   =\n"%str(level))
        ircsock.send("PRIVMSG "+ channel +" :===========================\n")
        
    
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server
    sendname=ircmsg.split("!")[0].strip(":")
    if len(sendname)<16:
        try:
            userstats[sendname.strip("_")]+=1
        except KeyError:
            print "new user added",sendname
            userstats[sendname.strip("_")]=0

    if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
        ping()
    host=""
    try:
        host=ircmsg.split("@")[1].split(" ")[0]
    except IndexError:
        pass
    if host=="REPLACETHISersc142.goemobile.de":
        msg=ircmsg.split(":")[2:]
        msg=":".join(msg)
        if msg[0]=="!":
            troll=["Du bist ein Klaus!","Lass mich, du Kotpfuetze","Ich schlafe gerade...","Donnerwetter","Koerperklaus"]
            rr=random.randint(0,4)
            ircsock.send("PRIVMSG "+ channel +" :"+troll[rr]+"\n")
    else:
        try: 
            msg=ircmsg.split(":")[2:]
            msg=":".join(msg)
            print "mymsg: %s"%msg
            if msg.find(botnick)>=0 and len(host)>0 and len(sendname)>0:
                ans=["Ja!","Ja","Nein","Auf keinen Fall!","Vielleicht...","Frag mich gleich nochmal","Hmm..."]
                rr=random.randint(0,len(ans)-1)
                ircsock.send("PRIVMSG "+ channel +" :"+ans[rr]+"\n")
            print msg[0]
            if msg[0]=="!" and msg[1:]=="date":
                now = datetime.datetime.now()
                ircsock.send("PRIVMSG "+ channel +" :"+now.strftime("%A, %d. %B %Y")+"("+now.strftime("%j")+"/~365)\n")
                exp+=1 
            if msg[0]=="!" and msg[1:]=="stats":
                ircsock.send("PRIVMSG "+ channel +" :"+"=========================================\n")
                ircsock.send("PRIVMSG "+ channel +" :"+"==================STATS==================\n")
                ircsock.send("PRIVMSG "+ channel +" :"+"=========================================\n")
                for key,entry in userstats.iteritems():
                    ircsock.send("PRIVMSG "+ channel +" :"+"= %16s  |         %5d     ="%(key,entry)+"\n")
                ircsock.send("PRIVMSG "+ channel +" :"+"=========================================\n")
                
                exp+=1 
            if msg[0]=="!" and (msg[1:]=="level" or msg[1:]=="lvl"):
                exp+=1  
                ircsock.send("PRIVMSG "+ channel +" :I am currently level "+str(level)+" and i have "+str(exp)+" exp!\n")
            if msg[0]=="!" and msg[1:]=="help":
                cmds=["help - shows this help",
                "date - shows the current date",
                "time - shows the current time",
                "mensaX - shows the menu for day X",
                "add xx:xx:xx <entry> - make an entry for time xx:xx:xx"
                ]
                for c in cmds:
                    ircsock.send("PRIVMSG "+ channel +" :"+c+"\n") 
                    exp+=1
            if msg[0]=="!" and msg[1:]=="time":
                now = datetime.datetime.now()
                ircsock.send("PRIVMSG "+ channel +" :Es ist "+now.strftime("%H:%M:%S")+" Uhr\n")  
                exp+=1
            if msg[0]=="!" and msg[1:6]=="mensa":
                mensalink="http://www.studentenwerk-goettingen.de/speiseplan.html?selectmensa=Nordmensa"
                try:
                    if int(msg[6])<5 and int(msg[6])>=1:
                        now = datetime.datetime.now()
                        mensalink+="&day="+str((int(msg[6])+1+days.index(now.strftime("%A")))%7)
                        if (int(msg[6])+1+days.index(now.strftime("%A")))%7 == 0:
                            ircsock.send("PRIVMSG "+ channel +" :[Mensa today]\n")  
                        else:
                            ircsock.send("PRIVMSG "+ channel +" :[Mensa "+days[((int(msg[6])+1+days.index(now.strftime("%A")))%7)-1]+"]\n")
                        #print mensalink
                except ValueError:
                    print "not a number"
                    continue
                except IndexError:
                    pass
                res=urllib2.urlopen(mensalink)
                res=res.read().strip('\n\r')
                app=res.split('<td class="ext_sits_speiseplan_rechts"><span class="ext_sits_essen">')
                if len(app)>1:
                    exp+=1
                    for i in range(1,len(app)):
                        if len(app[i].split("<strong>")[1].split("</strong>")[0]):
                            mens=h.unescape(app[i].split("<strong>")[1].split("</strong>")[0])
                            mens=''.join(mens.encode('utf-8'))
                            print mens
                            ircsock.send("PRIVMSG "+ channel +" :"+str(re.sub("\(.*\)","",mens))+"\n")  
                else:
                    ircsock.send("PRIVMSG "+ channel +" :Nix zu essen ;(\n")  
                    exp+=1
            if msg[0]=="!" and msg[1:4]=="add":
                sp=msg.split(" ",2)
                try:
                    if not (int(sp[1][0:2])>=0 and int(sp[1][0:2])<24):
                        raise ValueError
                    if not (int(sp[1][3:5])>=0 and int(sp[1][3:5])<60):
                        raise ValueError
                    if not (int(sp[1][6:8])>=0 and int(sp[1][6:8])<60):
                        raise ValueError
                    exp+=1
                    for ind,m in enumerate(lst):
                        if m[0]==sp[1]:
                            lst[ind]=(sp[1],m[1]+" / "+sp[2])
                            print "add: ",(lst[ind])
                            break
                        elif m==lst[-1]:
                            lst.append((sp[1],sp[2]))
                            print "append",lst[-1]
                            break
                except ValueError:
                    ircsock.send("PRIVMSG "+ channel +" : Dumb fool, format is: !add xx:xx:xx <name>, where xx are digits\n")
                    exp+=1
            if msg=="*** Checking Ident":
                print "starting threads..."
                time.sleep(20)
                thread.start_new_thread(bullshit,())
                thread.start_new_thread(msgs,())
                thread.start_new_thread(google,())
        except IndexError:
            pass
