'''

           test_<framework>.py
    
@summary:  Use this interface to add your favorite framework.
           Comparing (RAM usage) of different webframeworks.
           
@since:    5 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks

@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

'''

import <framework> #  pip install <framework>

HOST, PORT= '127.0.0.1', 8888 # default values

##############################################

@route('/hello/:name')
def index(name='Earth'):
    "Serve simple 'Hello World!' page, with default value if :name not given" 
    return 'Hello %s!' % name

def run_simplest():
    "start server with as little code as possible"
    <framework>.run()  
    
def run_server(host=HOST, port=PORT):
    "start server on host:port"
    print "<framework>" # if the starting server doesn't identify itself 
        
    <framework>.server(port=port, address=host)
    
##############################################
    
def url(host=HOST, port=PORT):
    "returns URL for testing"
    return "http://%s:%s/hello?name=World" % (host, port)

def version():
    "returns (name, version)"
    return ("tornado", <framework>.__version__ )

##############################################
    
if __name__ == '__main__':
    # run_simplest()
    
    # must be able to change port; get it from commandline argument
    from sys import argv as a; port=int(a[1]) if len(a)>1 else PORT 
    
    run_server(port=port)
    
    
    