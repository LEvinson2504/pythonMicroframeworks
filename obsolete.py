'''

           obsolete.py
    
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

import os, time, sys, multiprocessing, subprocess

import psutil # pip install psutil

import test_bottle, test_webpy, test_flask, test_cherrypy, test_tornado
from compare import measureMemory, killEm

WARNING = """

    WARNING

    startProcesses()
    
    Does start all the processes, yes. Works flawlessly, yes.
    
    BUT - the memory measurements are ~identical. 
    So ... useless. It seems to create full copies of the main process.
    
    instead use 'compare.py' -> startProcessesTotallyIndependent()
    """

def startProcesses(host="127.0.0.1", portstart=8000):
    """
    read WARNING
    
    """
    print "Start processes:"
    port=portstart
    processes=[]
    sleepBetween=0.3

    for module in ((test_bottle, test_webpy, test_flask, test_cherrypy, test_tornado)):
        run_server=getattr(module, 'run_server')
        v=getattr(module, 'version')
        url=getattr(module, 'url')
        
        p=multiprocessing.Process(target=run_server, args=(host, port))
        p.start()
        
        processes.append((p, "%s %s" % v(), url(host,port) ))
        port+=1
        
        if v()[0]=="cherrypy": time.sleep(2)
        elif v()[0]=="tornado": time.sleep(1) 
        else: time.sleep(sleepBetween)
        
    return processes

def measure1():
    "doesn't really work, because all processes have same size"
    processes=startProcesses()
    measureMemory(processes)
    killEm(processes)
    print WARNING
    
    
   
if __name__ == '__main__':
    measure1()
    # measure2()
    
    