'''

           test_webpy.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    4 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   to Kevin Veroneau. I based parts of this on his code snippets. 
           http://www.pythondiary.com/blog/Feb.14,2012/too-many-micro-webframeworks.html
           
'''

import web # pip install web.py

# HOST, PORT= '0.0.0.0', 8080
HOST, PORT= '127.0.0.1', 8080


urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'Earth'
        return 'Hello, ' + name + '!'

def run_simplest():
    app.run() 
    
def run_server(host=HOST, port=PORT):
    print "web.py:", 
    web.httpserver.runsimple(app.wsgifunc(), (host, port))
   
def url(host=HOST, port=PORT):
    return "http://%s:%s/World" % (host, port)

def version():
    return ("web.py", web.__version__)
    
if __name__ == '__main__':
    # run_simplest()
    
    from sys import argv as a; port=int(a[1]) if len(a)>1 else PORT # get port from commandline argument

    run_server(port=port)
    
    
    