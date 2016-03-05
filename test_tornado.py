'''

           test_tornado.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    5 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

'''


import tornado.ioloop, tornado.web #  pip install tornado
from tornado import version as tornadoversion

HOST, PORT= '127.0.0.1', 8888

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        name=self.get_argument("name", default="Earth")
        self.write("Hello, %s!" % name)
        
    # using parameters, because I haven't tried out dispatching
    # http://www.tornadoweb.org/en/stable/guide/structure.html#the-application-object

def make_app():
    return tornado.web.Application([
        (r"/hello", MainHandler),
    ])

def run_tornado_simplest():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    
def run_server(host=HOST, port=PORT):
    print "tornado" 
    import time; time.sleep(0.1) # only because of printing
    
    app = make_app()
    app.listen(port=port, address=host)
    tornado.ioloop.IOLoop.current().start()
    
def url(host=HOST, port=PORT):
    return "http://%s:%s/hello?name=World" % (host, port)

def version():
    return ("tornado", tornadoversion )
    
if __name__ == '__main__':
    # run_tornado_simplest()
    
    from sys import argv as a; port=int(a[1]) if len(a)>1 else PORT # get port from commandline argument
    
    run_server(port=port)
    
    
    