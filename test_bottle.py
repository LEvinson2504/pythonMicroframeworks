'''

           test_bottle.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    4 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   to Kevin Veroneau. I based parts of this on his code snippets. 
           http://www.pythondiary.com/blog/Feb.14,2012/too-many-micro-webframeworks.html
           
'''

from bottle import route, run, __version__ # pip install bottle

HOST, PORT= '127.0.0.1', 8080

@route('/hello/:name')
def index(name='World'):
    return 'Hello %s!' % name

def run_server(host=HOST, port=PORT):
    # run()
    run(host=host, port=port)
    
def url(host=HOST, port=PORT):
    return "http://%s:%s/hello/World" % (host, port)

def version():
    return ("bottle", __version__)
    
if __name__ == '__main__':
    # run_server()
    
    from sys import argv as a; port=int(a[1]) if len(a)>1 else PORT # get port from commandline argument
    
    run_server(port=port)
    