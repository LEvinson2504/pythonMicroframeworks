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

import os, time
import psutil
from multiprocessing import Process
import test_bottle

def memory_usage(PID=None):
    if PID==None: PID=os.getpid()
    process = psutil.Process(PID)
    # print "PID=%d"%os.getpid(), 
    print process.memory_info()
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

def startProcesses(host="localhost", portstart=8000):
    
    print "Memory main process: ", memory_usage()
    port=portstart
    processes=[]
    for fn,name in ((test_bottle.run_bottle,"bottle"),
               ):
        p=Process(target=fn, args=(host, port))
        p.start()
        processes.append((p,name))
        
    sleep=2
    print "processes started, waiting %s seconds:" % sleep
    time.sleep(sleep)
    
    for p,name in processes:
        print "%10s PID=%d mem=%4.2f MiB" % (name, p.pid, memory_usage(p.pid))  
    
    pid=os.getpid()
    print "%10s PID=%d mem=%4.2f MiB" % ("main", pid, memory_usage())
    
if __name__ == '__main__':
    startProcesses()
    
    