'''

           compare.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    4 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   to Kevin Veroneau. I based parts of this on his code snippets. 
           http://www.pythondiary.com/blog/Feb.14,2012/too-many-micro-webframeworks.html
           
'''

VERSION=                   "0.1.9"

import os, time, sys, multiprocessing, subprocess
import psutil # pip install psutil
import test_bottle, test_webpy, test_flask, test_cherrypy, test_tornado

def startProcessesTotallyIndependent(portstart=8000):
    """
    This one works. And the memory measurement is independent. Not like in 'obsolete.py'.
    
    This starts the processes as completely separate 'python name.py 8888' subprocesses.
    """ 
    
    print "Start processes:"
    processes=[]
    port=portstart
    sleepBetween=0.3
    
    for module_name in ("test_bottle", "test_webpy", "test_flask", "test_cherrypy", "test_tornado"):
        
        p=subprocess.Popen(["python", module_name+".py", "%d" % port]) # start the process
        
        module=globals()[module_name]                                # like 'import test_bottle'
        v, url = getattr(module, 'version'), getattr(module, 'url')  # like 'test_bottle.url'
        
        processes.append((p, "%s %s" % v(), url(port=port) )) # keep PID, and 
        
        # some of them need a bit longer to start:
        if v()[0]=="cherrypy": time.sleep(1.5)  
        elif v()[0]=="tornado": time.sleep(0.7) 
        else: time.sleep(sleepBetween)
        
        port += 1 # continue with one-up
        
    return processes
        


def memory_usage(pid=None):
    # if PID==None: PID=os.getpid() # default psutil behaviour anyways
    process = psutil.Process(pid)
    pmi=process.memory_info()
    rss = pmi.rss / float(2 ** 20)
    vms = pmi.vms / float(2 ** 20)
    return (rss, vms)

def measureMemory(processes):
    sleep=2
    time.sleep(sleep)
    print
    print "Waited %s seconds, measuring now." % sleep
    print 
    
    # 'posix', 'nt', 'os2', 'ce', 'java', 'riscos'.
    if os.name == 'nt': osname="Windows"
    if os.name == 'posix': osname="Posix" 

    formatter="%-18s %7s PID=%5d MEM(rss,vms)=(%4.2f,%6.2f) MiB  %s"
    
    for p, name, url in processes:
        mem=memory_usage(p.pid)
        print formatter % (name, osname, p.pid, mem[0], mem[1], url)  
    
    mem=memory_usage()
    print formatter % ("main "+VERSION, osname, os.getpid(), mem[0], mem[1], "")
    

def killEm(processes):
    print "\nKilling PIDs:", 
    for p, name, _ in processes:
        print "%d (%s)" % (p.pid, name),
        p.terminate()
    print

    

def measure2():
    processes=startProcessesTotallyIndependent()
    measureMemory(processes)
    killEm(processes)
    
if __name__ == '__main__':
    measure2()
    
    