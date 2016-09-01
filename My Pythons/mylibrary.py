import os, platform,sys,time,threading
from datetime import datetime

def mycompressor():
    f=open('pinglog.txt','r')
    myfile=f.read()
    f.close()
    cfile=open('pinglog_compressed.txt','w')
    mystr=myfile.split('\n')
    s=False
    e=False
    TFlist=[]
    for x in range(0,len(mystr)):
        if ('False' in mystr[x]) and (s==False):
            s=x
        if ('False' not in mystr[x]) and (s!=False):
            e=x
            TFlist=[]
            for i in range(s,e):
                TFlist.append(mystr[i][20:])
            TFstr=str(TFlist).replace('True','1').replace('False','0').replace('[','').replace(']','').replace(' ','').replace('\',\'','-').replace('\'','').replace(',','')
            cfile.write(mystr[s][0:10]+'  '+ mystr[s][11:19]+'-'+ mystr[e][11:19]+'   '+TFstr+'\n')
            s=False
            TFlist=[]
    cfile.write('HHH')
    print('HHH')
    cfile.close()
    t.start()
    return()

def myping():

    """
    Returns True if host responds to a myping request
    """
    host=['www.google.com','www.facebook.com','www.wikipedia.com','www.yahoo.com','www.orf.at']
    
    # myping parameters as function of OS
    myping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # myping
    answer=[]
    for i in range(0,len(host)):
        answer.append(os.system("ping " + myping_str + " " + host[i]) == 0)
        time.sleep(0.9)
    return(answer)


def mytime():
	mytime=datetime.now()	
	date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
	return(date)
