'''

           all.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    4 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   to Kevin Veroneau. I based parts of this on his code snippets. 
           http://www.pythondiary.com/blog/Feb.14,2012/too-many-micro-webframeworks.html
           
'''

VERSION=                   "0.1.0"

import os, time, sys
from multiprocessing import Process

import psutil # pip install psutil
# print psutil.__version__

import test_bottle, test_webpy, test_flask

def memory_usage(PID=None):
    # if PID==None: PID=os.getpid() # default psutil behaviour anyways
    process = psutil.Process(PID)
    # print process.memory_info()
    rss = process.memory_info().rss / float(2 ** 20)
    vms = process.memory_info().vms / float(2 ** 20)
    return (rss, vms)



def startProcesses(host="localhost", portstart=8000):
    
    print "Memory main process: ", memory_usage()
    print "Start processes:"
    port=portstart
    processes=[]
    sleepBetween=0.3
    
    """
    for fn, v, url in ((test_bottle.run_bottle, test_bottle.version, test_bottle.url),
                       (test_webpy.run_webpy, test_webpy.version, test_webpy.url),
                       ()):
       """
    for module in ((test_bottle, test_webpy, test_flask)):
        run_server=getattr(module, 'run_server')
        v=getattr(module, 'version')
        url=getattr(module, 'url')
        
        p=Process(target=run_server, args=(host, port))
        p.start()
        
        processes.append((p, "%s %s" % v(), url(host,port) ))
        port+=1
        
        time.sleep(sleepBetween)
        
    sleep=1
    time.sleep(sleep)
    print "Waited %s seconds." % sleep
    print 
    
    formatter="%-18s %7s PID=%5d MEM(rss,vms)=(%4.2f,%6.2f) MiB  %s"
    
    # 'posix', 'nt', 'os2', 'ce', 'java', 'riscos'.
    if os.name == 'nt': osname="Windows"
    if os.name == 'posix': osname="Posix" 
    
    for p, name, url in processes:
        mem=memory_usage(p.pid)
        print formatter % (name, osname, p.pid, mem[0], mem[1], url)  
    
    pid=os.getpid()
    mem=memory_usage()
    print formatter % ("main "+VERSION, osname, pid, mem[0], mem[1], "")
    
if __name__ == '__main__':
    startProcesses()
    
    