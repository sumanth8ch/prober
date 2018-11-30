#! /usr/bin/python
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
sysup = []
sysup1 = []
data = []
data1 = []
output = []
while (count < samples):
    t0 = time.time()
    try :
        session = Session(hostname = ip, remote_port = port, community = comm, version = 2, timeout = 3, retries = 1)
        data = session.get(oidlist)
        sysup = session.get('1.3.6.1.2.1.1.3.0')
    except easysnmp.exceptions.EasySNMPTimeoutError:
        continue
    t1 = time.time()
    if (count !=0):
        if sysup[0] < sysup1[0]:
            print("SYSTEM REBOOTED")
            data = []
            data1 = []
            sysup = []
            sysup1 = []
            output = []
        else :
            continue
    t2 = t1-t0
    if(count==0):
        count += 1
    else:
        for i in range(len(oidlist)):
            p = int(data[i].value)
            q = int(data1[i].value)
            cnttype = str(data[i].snmp_type)
            rate = (p-q)/t2
            if rate<0:
                if cnttype == 'COUNTER':
                    rate = ((p+2**32)-q)/t2
                    output.append(rate)
                elif cnttype == 'COUNTER64':
                    rate = ((p+2**64)-q)/t2
                    output.append(rate)
            else :
                output.append(rate)
        count += 1
    if(len(output==0)):
        print (t1, "|")
    else:
        for i in output:
            print (t1, "|", ("|".join(i)))
    data1 = data[:]
    sysup1 = sysup[:]
    del output[:]
    t3 = time.time()
    if(interval > (t3-t2)):
        t4 = interval - (t3-t2)
        time.sleep(t4)
    else:
        continue
