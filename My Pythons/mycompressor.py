f=open('pinglog.txt','r')
myfile=f.read()
f.close()
mystr=myfile.split('\n')
s=False
e=False
for x in range(0,len(mystr)):
    if ('False' in mystr[x]) and (s==False):
        s=mystr[x][0:20]
    if ('False' not in mystr[x]) and (s!=False):
        e=mystr[x-1][0:20]
        print(s[0:10],'  ', s[11:-1],'-', e[11:-1], '   ', mystr[x-1][20:])
        s=False
