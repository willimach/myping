def ping(host):
    import os, platform, sys
    #Returns True if host responds to a ping request
    # Ping parameters as function of OS
    # -c 1: send 1 package -w 1 wait 1 s for answer
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1 -w 1 -q"
    # Ping    
    answer=(os.system("ping " + ping_str + " " + host) == 0)
    return(answer)

def mytime():
    import time, datetime
    mytime=datetime.datetime.now()
    unixtime=round(time.time())
    date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
    return(date,unixtime)

def mycompressor():
    #print('compressing...')
    f=open('pinglog.txt','r')
    myfile=f.read()
    f.close()
    open('pinglog.txt','w').close() # delete file content
    cfile=open('pinglog_compressed.txt','a')
    mystr=myfile.split('\n')
    s=False     # startline www down
    e=False     # end
    urlset={'0','1','2','3','4'}
    for x in range(0,len(mystr)):
        if ('False' in mystr[x]) and (s==False):
            s=x
        if ('False' not in mystr[x]) and (s!=False):
            e=x
            TFstr=''   #TrueFalseList
            #extract Thread(=URL)-numbers
            for i in range(s,e):
                TFstr=TFstr+ mystr[i][26:]
            #wenn alle server down -> write in file
            if set(str(TFstr))==urlset:
                if len(mystr[s][0:10])==10 and len(mystr[s][11:19])==8 and len(mystr[e][11:19])==8:
                    cfile.write(mystr[s][0:10]+'  '+ mystr[s][11:19]+'-'+ mystr[e][11:19]+ '\t'+ 'down!'+'\n')
                else:
                    logfile=open('logfile.txt', 'a')
                    logfile.write(mystr[s][0:10]+'  '+ mystr[s][11:19]+'-'+ mystr[e][11:19]+ '\t'+ 'down!'+'\n')
                    logfile.close()
            # letztes Element in mystr ist immer leer. Falls genau während eines Ausfalls komprimiert wird, wird hier
            # Endzeit definiert
            #if set(str(TFstr))==urlset and mystr[x]== '':
            #   cfile.write(mystr[s][0:10]+'  '+ mystr[s][11:19]+'-'+ mystr[e-1][11:19]+ '\t'+ 'down!'+'\n')

            s=False
            TFlist=[]
    cfile.close()
    
#extrahiert aus pinglog_compressed anfangszeitpunkt und dauer des ausfalls in Minuten (grob)
def t_ext(line):
    h1,m1,s1=int(line[12:14]),int(line[15:17]),int(line[18:20])
    h2,m2,s2=int(line[21:23]),int(line[24:26]),int(line[27:29])
    
    minutes=h1*60+m1
    length=(h2-h1)*60+(m2-m1)
    #aufrunden:
    if length< 1:
        length=1
    #print(h1,m1,s1,'\n',h2,m2,s2,'\n',minutes/60,length/60)
    return(round(minutes/60,2),round(length/60,2))

def plotter():
    # Force matplotlib to not use any Xwindows backend.
    import matplotlib, numpy, datetime
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,date2num,num2date
    import gc
    
    f=open('pinglog_compressed.txt','r')
    myfile=f.read()
    mylines=myfile.split('\n')
    mylines.pop(-1)

    
    #20 inch in x, pro 3 Messungen ein inch
    fig, ax = plt.subplots(figsize=(22,len(mylines)//3))

    if len(mylines)>40: #plot just 40 lines
         ystart=len(mylines)-30
    else:
         ystart=1
         
    for i in range(ystart,len(mylines)):
        ax.broken_barh([t_ext(mylines[i])],(date2num(datetime.datetime(int(mylines[i][0:4]),int(mylines[i][5:7]),int(mylines[i][8:11])))-0.45,0.9),facecolors='black')
        #print(t_ext(mylines[i]))

    ax.set_xlim(0,24)
    #anfangs/endtag für y-Achse:    
    date1 = datetime.datetime(int(mylines[ystart][0:4]),int(mylines[ystart][5:7]),int(mylines[ystart][8:11]))
    date2 = datetime.datetime(int(mylines[-1][0:4]),int(mylines[-1][5:7]),int(mylines[-1][8:11]))
    ax.set_ylim(date1, date2)
    ax.grid(True)
    major_ticks = numpy.arange(0, 24, 1)    
    ax.set_xticks(major_ticks)
    ax.yaxis.set_major_locator(DayLocator())
    ax.yaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.fmt_ydata = DateFormatter('%Y-%m-%d %H:%M:%S')    
    plt.title('FGG36 offline times' + '  '*40 + mytime()[0],loc='right')

    plt.savefig('offline.png',bbox_inches='tight')

    plt.clf()
    plt.close()
    del date1, date2, major_ticks
    gc.collect()

def myftp():
    from ftplib import FTP
    import configparser

    config=configparser.ConfigParser()
    config.read('ping_config.txt')

    server=config['FTP']['server']
    user=config['FTP']['user']
    passwd=config['FTP']['passwd']

    ftp=FTP(server,user=user,passwd=passwd)
    file=open('offline.png','rb')
    ftp.cwd('www')
    ftp.storbinary('STOR offline.png',file)
    file.close()
    ftp.quit()
