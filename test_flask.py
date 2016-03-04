'''

           test_flask.py
    
@summary:  Comparing (RAM usage) of different webframeworks
@since:    4 Mar 2016
@author:   Andreas
@home      github.com/drandreaskrueger/pythonMicroframeworks
@license:  MIT but please donate:
@bitcoin:  14EyWS5z8Y5kgwq52D3qeZVor1rUsdNYJy

@thanks:   to Kevin Veroneau. I based parts of this on his code snippets. 
           http://www.pythondiary.com/blog/Feb.14,2012/too-many-micro-webframeworks.html
           
'''

from flask import Flask, __version__ # pip install Flask
app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name="Earth"):
    return "Hello %s!" % name

def run_flask_simplest():
    app.run()
    
def run_server(host='127.0.0.1', port=5000):
    app.run(host=host, port=port)
    
def url(host='127.0.0.1', port=5000):
    return "http://%s:%s/hello/World" % (host, port)

def version():
    return ("flask", __version__)
    
if __name__ == '__main__':
    print "%s %s" % version()
    print "try:", url()
    # run_flask_simplest()
    run_server()
    
    