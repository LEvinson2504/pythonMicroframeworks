'''

           test_cherrypy.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    5 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   to Kevin Veroneau. I based parts of this on his code snippets. 
           http://www.pythondiary.com/blog/Feb.14,2012/too-many-micro-webframeworks.html
           
'''

import cherrypy # pip install cherrypy

HOST, PORT= '127.0.0.1', 8080

class HelloWorld(object):
    def index(self, name="Earth"):
        return "Hello %s!" % name
    index.exposed = True
    
    # using parameters, because I haven't tried out dispatching
    # https://cherrypy.readthedocs.org/en/3.2.6/concepts/dispatching.html

def run_cherrypy_simplest():
    cherrypy.quickstart(HelloWorld())
    
   
def run_server(host=HOST, port=PORT):
    print "CherryPy" 
    import time; time.sleep(0.1) # only because of printing
    
    cherrypy.config.update({'server.socket_host': host,
                            'server.socket_port': port,})
    
    cherrypy.quickstart(HelloWorld(), config={'/': {'tools.gzip.on': True}} )
    
    
def url(host=HOST, port=PORT):
    return "http://%s:%s/?name=World" % (host, port)

def version():
    return ("cherrypy", cherrypy.__version__)
    
if __name__ == '__main__':
    # run_cherrypy_simplest()
    
    from sys import argv as a; port=int(a[1]) if len(a)>1 else PORT # get port from commandline argument
    
    run_server(port=port)
    
    