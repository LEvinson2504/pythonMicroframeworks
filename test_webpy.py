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
    app.run(port=port)
    
def run_webpy(host="localhost", port=8080):
    print "web.py:", 
    web.httpserver.runsimple(app.wsgifunc(), (host, port))
   
def url(host='localhost', port=8080):
    return "http://%s:%s/World" % (host, port)

def version():
    return web.__version__
    
if __name__ == '__main__':
    #print "%s %s" % version()
    #print "try:", url()
    run_webpy()
    
    