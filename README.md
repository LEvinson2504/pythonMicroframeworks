# pythonMicroframeworks
comparison of (memory & speed of) 
* bottle 
* cherrypy 
* Flask 
* tornado 
* web.py

Each can be started standalone (see ``test_frameworkname.py``), and serves a "Hello World!" to the browser.
 
### Quickstart

Dependencies - Prepare machine with tools and python pip; and upgrade pip, and install all frameworks:

    apt-get update && apt-get install -y git nano sudo python-pip build-essential python-dev
    pip install -U pip && pip install bottle cherrypy Flask tornado web.py psutil requests
    
(tested in the cloud, on Debian 8 [Digitalocean VPS](https://m.do.co/c/f934b16d6302) - bookmark [my superb manual](https://github.com/drandreaskrueger/buyme/blob/master/_how-to/VPS.md) how to initialize & install django there.) 
    
Get my (comparison & 5 servers) sourcecode:

    git clone https://github.com/drandreaskrueger/pythonMicroframeworks.git
    cd pythonMicroframeworks
    
**Start comparison with**

    python compare.py 
    
    
### Commandline arguments
If -for hammering- you want more repetitions (per framework) and different timeout (in seconds):

    python compare.py 2000
    python compare.py 2000 0.5
    

### Results

Put 
* [results_windows.txt](results_windows.txt)
* [results_linux.txt](results_linux.txt)

besides each other in two windows, for now. (ToDo: Everything into one table.)

#### Strange
Memory measurement via ``psutil``:
* There is a big discrepancy between ``rss``, and ``vms`` on Linux and Windows.
* To me it looks as if ``Linux.rss ~= Windows.vms``. Strange - but the numbers are too close to not notice that. 
* See [psutil](http://pythonhosted.org/psutil/#psutil.Process.memory_info) tool. Hopefully, psutil 4.0.0 [will be more useful](http://pythonhosted.org/psutil/#psutil.Process.memory_full_info). My 3.3.0 does not have ``memory_full_info()`` yet.

#### Main findings
* Most of my measurements show more memory usage than this [2011 examination](http://nuald.blogspot.de/2011/08/web-application-framework-comparison-by.html) - but those were older versions.
* *web.py* is slower, especially on Windows, hammering takes ~60% longer as for any of the others.
* *web.py* is the first to timeout on *Windows*.
* *tornado* is the first to timeout on *Linux*.
* After hammering (2000 requests per framework), the memory usage is higher.
  * for *bottle*, the effect is < 1%. *Bottle seems to have the best memory management.*
  * *all* the other frameworks need considerably more memory after having served 2000 url requests.
  * the effect is stronger on *Windows* for most of them. 
  * for *tornado* the effect is stronger on *Linux* - it needs 23% more memory after 2000 url requests.
* Some of the frameworks are probably really powerful, but also more difficult to understand. And ...

... before my final verdict, I guess I need to sleep. This was ~9 hours of straight coding. *After* a full working day. :-) 
  

### You
Please help, fork it, improve it. It was a one-night-hack. Not everything is super-elegant yet. But it works.  
***NEW:*** You can actually [include your favorite webframework](test_framework.py) now, easily.  

Please [retweet](https://twitter.com/drandreaskruger/status/706103743482368001) or [probably better this one](https://twitter.com/drandreaskruger/status/706115609394868226), thx. 

## Donationware
Very important - **If you like this, show it:** `` [BTC] 14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy ``. Thanks, much appreciated.  
*No Coinbase account yet?* Then [use my referral](https://www.coinbase.com/join/andreaskrueger), to give me and you 10$ bonus.  Oh yes, you can also hire me, part time.


