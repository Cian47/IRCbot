#essential
import thread
from Queue import *


#for mod
#import distance
import gzip
import time
import Stemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

class abb0t(object):
    de=Stemmer.Stemmer("german")
    en=Stemmer.Stemmer("english")
    
    def __init__(self, nick):
        self.queue_in=Queue()
        self.queue_out=Queue()
        thread.start_new_thread(self.run,())
        self.resttime=0
        self.lastcmd=0
        self.nick=nick
        self.logfile="msglogabb0t.gz"
        self.blacklist=["bottle","Abb0t","Ezrael"]
        self.msgblacklistfile="msgblacklist.gz"
        self.msgblacklist=gzip.open(self.msgblacklistfile).read().lower().strip("\n").split("\n")
        self.ziplines=gzip.open(self.logfile).read().strip("\n").split("\n")
        self.all_msgs=[]
        tmp=[]
        for line in self.ziplines:
            l=line
            l=l.lower().strip("\t\n \r,").split(";",2)
            if l[1] not in self.blacklist and len(l[2])>0 and l[2][0]!="!":
                try:
                    self.all_msgs.append(abb0t.de.stemWord(l[2].decode("utf-8")))
                except UnicodeDecodeError:
                    self.all_msgs.append(abb0t.de.stemWord(l[2].decode("iso-8859-1")))
                tmp.append(line)
        self.ziplines=tmp
        
            
        #self.vectorizer = TfidfVectorizer(min_df=1)#CountVectorizer(min_df=1)
        self.vectorizer = CountVectorizer(min_df=1)
        self.X = self.vectorizer.fit_transform(self.all_msgs)
        
    
    def run(self):
        while 1:
            recv=self.queue_in.get()
            try:
                _, msg_header, msg_payload = recv.split(":",2)
                identification, msg_type, msg_receiver = msg_header.strip(" ").split(" ")
                sender=identification.split("!")
                
                ##log messages. but with rules.
                if msg_payload and msg_receiver[0]=="#" and msg_payload.lower().find("abb0t")==-1 and msg_payload.lower().find("abbot")==-1 and sender not in self.blacklist:
                    with gzip.open(self.logfile,"a+") as log:
                        print "abb0tlogged:",msg_payload
                        log.write(str(time.time())+";"+sender[0]+";"+msg_payload+"\n")
                        
                        
                #if name is mentioned
                print self.msgblacklist
                if (msg_payload.lower().find(self.nick.lower())!=-1 or msg_payload.lower().find(self.nick.replace("0","o").lower())!=-1) and msg_receiver[0]=="#":
                    self.messagesTime=time.time()
                    if time.time() - self.lastcmd > self.resttime:
                        self.lastcmd=time.time()
                        
                        msg_payload=msg_payload.lower().replace("abb0t","").replace("abbot","")
                        t=self.vectorizer.transform([msg_payload]).toarray()[0]
                        
                        min_i=[99999999,-1,""]
                        for i,t2 in enumerate(self.X.toarray()):
                            w=cosine(t,t2)
                            if abs(w)<=min_i[0]:
                                if min_i[0]==w:
                                    if min_i[0]*1.0/len(self.all_msgs[min_i[1]]) > w*1.0/len(self.all_msgs[i]):
                                        print self.all_msgs[min_i[1]],">",self.all_msgs[i]
                                        min_i[1]=i
                                        min_i[2]=self.all_msgs[i]
                                else:
                                    print "new...",self.all_msgs[i],w
                                    min_i[0]=w
                                    min_i[1]=i
                                    min_i[2]=self.all_msgs[i]
                        
                        if min_i[1]==-1:
                            print "not saying anything, -1 ;)"
                            continue
                        print min_i
                        cmpcnt=self.ziplines[min_i[1]].strip("\t\n \r,").split(";",2)
                        print cmpcnt
                        
                        for k in xrange(min_i[1],min_i[1]+10):#len(self.ziplines)):
                            #print k
                            cnt=self.ziplines[k].strip("\t\n \r,").split(";",2)
                            print cnt
                            if cnt[2].lower() not in self.msgblacklist and len(cnt[2])>=3 and cnt[1] != cmpcnt[1] and cnt[2][0]!="!" :#and cnt[2].lower().find("abbot")==-1 and cnt[2].lower().find("abb0t")==-1:
                                if cnt[1] not in self.blacklist:
                                #print self.ziplines[k-1:k+2]
                                    self.queue_out.put("PRIVMSG "+ msg_receiver +" :"+sender[0]+": "+cnt[2].strip(" ,\t\n\r")+"\n")
                                    break
                                else:
                                    print "no answer ;)"
                        
                    else:
                        self.queue_out.put("PRIVMSG "+ msg_receiver +" : - I need a total rest of %d seconds - \n"%self.resttime)
                    
                
                #if msg_payload and msg_receiver[0]=="#":
                #    print "appendlogged:",msg_payload
                #    self.ziplines.append(str(time.time())+";"+sender[0]+";"+msg_payload+"\n")
                        
                
            except IndexError:
                print "IndexError"
                pass
            except ValueError: # no normal channel/private message
                print "ValueError"
                pass


    def cmd(self,msg):
        self.queue_in.put(msg)
