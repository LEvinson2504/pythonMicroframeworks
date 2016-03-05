# pythonMicroframeworks
comparison of (memory usage of) 
* bottle 
* cherrypy 
* Flask 
* tornado 
* web.py
 
 
### Usage

Prepare machine with tools and python pip; and upgrade pip, and install all frameworks:

    apt-get update && apt-get install -y git nano sudo python-pip build-essential python-dev
    pip install -U pip && pip install bottle cherrypy Flask tornado web.py psutil requests
    
Get my sourcecode:

    git clone https://github.com/drandreaskrueger/pythonMicroframeworks.git
    cd pythonMicroframeworks
    
**Start with**

    python compare.py 
    
    
### Commandline arguments
If -for hammering- you want more repetitions (per framework) and different timeout (in seconds):

    python compare.py 2000
    python compare.py 2000 0.5
    

### Results

See
* [results_windows.txt](results_windows.txt)
* [results_linux.txt](results_linux.txt)

#### Main findings:
* There is a big discrepancy between ``rss``, and ``vms`` memory usage on Linux and Windows, see [psutil](http://pythonhosted.org/psutil/#psutil.Process.memory_info) tool. Hopefully, psutil 4.0.0 [will be more useful](http://pythonhosted.org/psutil/#psutil.Process.memory_full_info), my 3.3.0 does not have ``memory_full_info()`` yet.
* All my measurements show much more memory usage than in this [2011 examination](http://nuald.blogspot.de/2011/08/web-application-framework-comparison-by.html) - but those were older versions, too.
* *web.py* is slower, especially on Windows, hammering takes ~60% longer as for any of the others.
* *web.py* is the first to timeout on windows.
* *tornado* is the first to timeout on Linux.
* After hammering, the memory usage is higher.
  * only for *bottle*, the effect is < 1%. *Bottle seems to have the best memory management.*
  * *all* the other frameworks need considerably more memory after 2000 url requests.
  * the effect is stronger on *Windows* for most of them. 
  * for *tornado* the effect is stronger on *Linux*, it needs 23% more memory after 2000 url requests.
  
Please help me improve this. It was a one-night-hack. Not everything is super-elegant yet. But it works.

## Donationware
If you like this, show it: ``[BTC] 14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy``. Thanks, much appreciated.



