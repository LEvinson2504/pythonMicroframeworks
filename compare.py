'''

           compare.py
    
@summary:  Comparing (RAM usage) of different webframeworks

@since:    4 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks

@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   also see these older memory measurements:
           http://nuald.blogspot.de/2011/08/web-application-framework-comparison-by.html
'''

VERSION=                   "0.4.2"

import os, time, sys, subprocess, threading
from collections import Counter
import psutil   # pip install psutil
import requests # pip install requests

# mine:
import test_bottle, test_webpy, test_flask, test_cherrypy, test_tornado

# add yours here (plus see 'test_framework.py')
FRAMEWORKS = ("bottle", "webpy", "flask", "cherrypy", "tornado")
# pip install psutil requests bottle cherrypy Flask tornado web.py

# for hammering:
REPETITIONS=800
TIMEOUT=1.0

NAME=os.path.split(__file__)[-1]

def startProcessesTotallyIndependent(portstart=8000, stdout=sys.stdout, stderr=sys.stderr):
    """
    Start all the frameworks, and return their (process, name&version, and url).
     
    This one works. And the memory measurement is independent. Not like in 'obsolete.py'.
    This starts the processes as completely separate 'python name.py 8888' subprocesses.
    """ 
    
    print "Started these independent subprocesses:", 
    processes=[]
    port=portstart
    sleepBetween=0.3
    
    for framework in FRAMEWORKS:
        
        module_name="test_%s" % framework
        
        # start the process
        p=subprocess.Popen(["python", module_name+".py", "%d" % port], 
                           stdout=stdout, stderr=stderr) 
        
        module=globals()[module_name]                                 # like 'import test_bottle'
        v, url = getattr(module, 'version'), getattr(module, 'url')   # like 'url=test_bottle.url'
        
        processes.append([ p,               # keep PID,
                          "%s %s" % v(),    # and name version, 
                          url(port=port)] ) # and url
        
        # some of them need a bit longer to start, sleepwait for clustered log printing
        if v()[0]=="cherrypy": time.sleep(1.0)  
        elif v()[0]=="tornado": time.sleep(0.5) 
        else: time.sleep(sleepBetween)
        
        print "%s (%d)" % (framework, p.pid), 
        port += 1 # continue with one-up
        
    print
    return processes


def memory_usage(pid=None):
    """
    The first 2 numbers from memory_info. Converted to MiB.
    Strangely different on Windows & Linux. See README.md
    """ 
    # if PID==None: PID=os.getpid() # default psutil behaviour anyways
    # print psutil.__version__
    process = psutil.Process(pid)
    pmi=process.memory_info()
    rss = pmi.rss / float(2 ** 20)
    vms = pmi.vms / float(2 ** 20)
    return (rss, vms)

def measureMemory(processes):
    """
    show table
    one line for each process == framework
    with name&version, OS, PID, memory usage, url 
    """  
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
    print formatter % (NAME+" "+VERSION, osname, os.getpid(), mem[0], mem[1], "")
    

####################

def killEm(processes):
    """Don't leave zombie processes."""
    
    print "\nKilling PIDs:", 
    for p, name, _ in processes:
        print "%d (%s)" % (p.pid, name),
        p.terminate()
    print

####################

def hammer_thread(url, results, timeout):
    """
    inside one thread: get url, store status_code, 
    e.g. 200==OK, or -1 for exception raised
    """
    try:
        response = requests.get(url, timeout=timeout)
    except Exception as e:
        # print type(e), e
        results.append(-1)
    else:
        results.append(response.status_code)


def hammer(url, rep, timeout=TIMEOUT):
    """
    Start 'rep' such threads.
    Measure total time. Return histogram (Counter) of status_codes. 
    """
    T=time.time()
    threads, results = [],[]
    for _ in range(rep):
        t=threading.Thread(target=hammer_thread, args=(url, results, timeout))
        t.start()
        threads.append(t)
    for t in threads: t.join()
    
    duration = time.time()-T
    return duration, Counter(results)
    
def test_hammer(rep=REPETITIONS):
    """DOS attack on google :-)"""
    
    url="http://www.google.de"
    t,C=hammer(url, rep)
    rate=float(C[200])/sum(dict(C).values()) # percentage of http response 200 == OK
    print "%5.1f seconds with %5.1f%% success rate - %s"% (t, 100*rate, C)

def hammerLocalhost(processes, rep=REPETITIONS, timeout=TIMEOUT):
    """
    Hammer all frameworks, one after the other.
    Show results. Now it is good that we've redirected stdout&stderr.
    """
    
    print"\nNow hammering each of those servers ",
    print "%d times, with a %.3f seconds timeout: " % (rep, timeout), 
    sys.stdout.flush()
    time.sleep(1)
    
    results=[]
    T=time.time()
    
    for _, name, url in processes:
        m={}
        m["name"], m["url"] = name, url
        m["time"], m["Counter"] = hammer(url, rep, timeout=timeout)
        results.append(m)
        print m["name"].split(" ")[0], 
        
    print "- Done."
    print "Concurrent hammering %d * %d urls took %4.1f secs." % (len(processes), rep, time.time() - T),
    print "Results: (200 = OK; -1 = exception, probably 'requests.exceptions.ReadTimeout')"
    print
    
    for m in results:
        print "%-16s %40s" % (m["name"], m["url"]), 
        rate=float(m["Counter"][200])/sum(dict(m["Counter"]).values())
        print "  took %.4f seconds/call, with %5.1f%% success - %s"% (m["time"]/rep, 100*rate, m["Counter"])

####################

def measure2(rep=REPETITIONS, timeout=TIMEOUT):
    """
    The whole thing:
      Start processes.
      Measure memory.
      Hammer servers.
      Measure memory.
      Kill processes.
    """
     
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
    # print memory_usage(); exit()
    # test_hammer(rep=100); exit() 
    
    from sys import argv as a
    rep    =  int(a[1]) if len(a)>1 else REPETITIONS 
    timeout=float(a[2]) if len(a)>2 else TIMEOUT
    
    measure2(rep=rep, timeout=timeout)
    
    