#!/usr/bin/python
import easysnmp, sys, time
from easysnmp import Session
agentdetails = sys.argv[1].split(':')
ip = agentdetails[0]
port = int(agentdetails[1])
comm = agentdetails[2]
sampfreq = float(sys.argv[2])
interval = 1/sampfreq
samples = int(sys.argv[3])
oidlist = sys.argv[4:len(sys.argv)]
count = 0
sysup1 = []
sysup2 = []
data1 = []
data2 = []
output=[]
tempt = 0
x=[]

while (count <= samples):
    t1 = time.time()
    try :
        session = Session(hostname = ip, remote_port = port, community = comm, version = 2, timeout = 3, retries = 1)
        data1 = session.get(oidlist)
        sysup1 = session.get('1.3.6.1.2.1.1.3.0')
    except easysnmp.exceptions.EasySNMPTimeoutError:
        pass
    t2 = time.time()
    
    if len(data1) == len(data2):
        if sampfreq > 1 :
            t = sysup1 - sysup2
        if sampfreq <= 1 :
            temp =  t1 - tempt
            if temp != 0 :
                t = temp
            else:
                t = interval

        for i in range(len(oidlist)):
		    p = int(data1[i].value)
		    q = int(data2[i].value)
		    cnttype = str(data1[i].snmp_type)
		    if p>=q:
		        rate = (p-q)/t
		        output.append(rate)
		    if p<q and cnttype == 'COUNTER64':
		        rate = ((2**64+p)-q)/t
		        output.append(rate)
		    if p<q and cnttype == 'COUNTER32':
		        rate =  ((2**32+p)-q)/t
		        output.append(rate)
    count = count + 1
    if(len(output)==0):
        pass
    else:
        x = [str(i) for i in output]
        print t1, "|", ("|".join(x))
    data2 = data1[:]
    sysup2 = sysup1
    del output[:]
    tempt = t1
    t3 = time.time()
    if(interval > (t3-t1)):
        t4 = interval - (t3-t1)
        time.sleep(t4)
    else:
        time.sleep(0.0)
