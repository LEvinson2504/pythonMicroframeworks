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
           
           also see these memory measurements:
           http://nuald.blogspot.de/2011/08/web-application-framework-comparison-by.html
'''

VERSION=                   "0.2.0"

import os, time, sys, multiprocessing, subprocess, threading
import psutil # pip install psutil
import requests # pip install requests

from collections import Counter

import test_bottle, test_webpy, test_flask, test_cherrypy, test_tornado

def startProcessesTotallyIndependent(portstart=8000, stdout=sys.stdout, stderr=sys.stderr):
    """
    This one works. And the memory measurement is independent. Not like in 'obsolete.py'.
    
    This starts the processes as completely separate 'python name.py 8888' subprocesses.
    """ 
    
    print "Started independent subprocesses:", 
    processes=[]
    port=portstart
    sleepBetween=0.3
    
    for framework in ("bottle", "webpy", "flask", "cherrypy", "tornado"):
        
        module_name="test_%s" % framework
        
        # start the process
        p=subprocess.Popen(["python", module_name+".py", "%d" % port], 
                           stdout=stdout, stderr=stderr) 
        
        module=globals()[module_name]                                # like 'import test_bottle'
        v, url = getattr(module, 'version'), getattr(module, 'url')  # like 'test_bottle.url'
        
        processes.append([ p, "%s %s" % v(), url(port=port)] ) # keep PID, and name, and url
        
        # some of them need a bit longer to start, sleepwait for clustered printing
        if v()[0]=="cherrypy": time.sleep(1.0)  
        elif v()[0]=="tornado": time.sleep(0.5) 
        else: time.sleep(sleepBetween)
        
        print framework,
        port += 1 # continue with one-up
        
    print
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
    print "Waited %s seconds, measuring memory consumption now:" % sleep
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
    

####################

def killEm(processes):
    print "\nKilling PIDs:", 
    for p, name, _ in processes:
        print "%d (%s)" % (p.pid, name),
        p.terminate()
    print

####################

def hammer_thread(url, results, timeout):
    try:
        response = requests.get(url, timeout=timeout)
    except Exception as e:
        # print type(e), e
        results.append(-1)
    else:
        results.append(response.status_code)

TIMEOUT=20
    
def hammer(url, rep, timeout=TIMEOUT):
    T=time.time()
    threads, results = [],[]
    for _ in range(rep):
        t=threading.Thread(target=hammer_thread, args=(url, results, timeout))
        t.start()
        threads.append(t)

    for t in threads: t.join()
    duration = time.time()-T
    return duration, Counter(results)
    

REPETITIONS=10

def test_hammer(rep=REPETITIONS):
    url="http://www.google.de"
    t,C=hammer(url, rep)
    
    rate=float(C[200])/sum(dict(C).values()) # percentage of http response 200 == OK
    print "%5.1f seconds with %5.1f%% success rate - %s"% (t, 100*rate, C)

def hammerLocalhost(processes, rep=REPETITIONS, timeout=TIMEOUT):
    print"\nNow hammering each of those servers %d times, with a %.1f seconds timeout: " % (rep, timeout), 
    time.sleep(1)
    
    results=[]
    T=time.time()
    
    for _, name, url in processes:
        m={}
        m["name"], m["url"] = name, url
        m["time"], m["Counter"] = hammer(url, rep, timeout=timeout)
        results.append(m)
        print m["name"].split(" ")[0], 
        
    print "- Done"
    print "Concurrent hammering %d * %d urls took %4.1f secs." % (len(processes), rep, time.time() - T),
    print "Results: (200 = OK; -1 = exception, probably 'requests.exceptions.ReadTimeout')"
    print
    
    for m in results:
        print "%-16s %40s" % (m["name"], m["url"]), 
        rate=float(m["Counter"][200])/sum(dict(m["Counter"]).values())
        print "  took %.4f seconds/call, with %5.1f%% success - %s"% (m["time"]/rep, 100*rate, m["Counter"])

####################

def measure2(rep=REPETITIONS, timeout=TIMEOUT):
    f=open("logging.txt", "w")
    stdout=stderr=f
    
    processes=startProcessesTotallyIndependent(stdout=stdout, stderr=stderr)
    
    measureMemory(processes)
    
    hammerLocalhost(processes, rep=rep, timeout=timeout)
    
    for i in range(len(processes)):processes[i][2]="" # we don't need the urls anymore
    
    print "\nNow after all those calls, measure memory again ... ", 
    measureMemory(processes)
    
    killEm(processes)
    f.close()
    
if __name__ == '__main__':
    # test_hammer()
    
    measure2(rep=800, timeout=1)
    
    