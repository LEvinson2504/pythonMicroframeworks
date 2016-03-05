# pythonMicroframeworks
comparison, memory usage
 
    pip install psutil requests bottle cherrypy Flask tornado web.py
    git clone https://github.com/drandreaskrueger/pythonMicroframeworks.git
    cd pythonMicroframeworks
    
start with

    python compare.py
    
of if -for hammering- you want more repetitions (per framework) and different timeout (in seconds):

    python compare.py 2000
    python compare.py 2000 3
    