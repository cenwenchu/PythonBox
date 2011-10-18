'''
Created on 2011-9-27

@author: fangweng

support data dragger from local file by http request

command=pulllog&size=5000&logfile=/Users/apple/Documents/workspace/PythonBox/src.test/test.log&from=tip
command=mark&logfile=/Users/apple/Documents/workspace/PythonBox/src.test/test.log&from=tip&tag=tag1
command=goto&logfile=/Users/apple/Documents/workspace/PythonBox/src.test/test.log&from=tip&tag=tag1

'''

import BaseHTTPServer,SocketServer,os,sys,threading

class DraggerHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    fileIndexKeeper = dict()
    fileMarkKeeper = dict()
    
    indexLock = threading.Lock()
    markLock = threading.Lock()
    
    def __init__(self, request, client_address, server):
        self.params = dict()
        self.result = True
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
    
    def do_GET(self):
        req_content = self.requestline[self.requestline.index("?") + 1:].split(" ")[0]
        self.parseContent2Params(req_content)
        self.innerProcess()
        

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))    
        req_content = self.rfile.read(length)
        self.parseContent2Params(req_content)
        self.innerProcess()
        
        
    def parseContent2Params(self,content):
        ps = content.split("&")
           
        for p in ps:
            self.params[p[:p.index("=")]]= p[p.index("=")+1:]
            
        if ("command" not in self.params) or ("logfile" not in self.params):
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("need command and logfile param")
            self.result = False
            
        self._command = self.params.get("command")
        self._logfile = self.params.get("logfile")
        self._from = "_default"
        self._size = 1000
            
        if ("tag" not in self.params and (self._command == "mark" or self._command == "goto" )):
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("command mark or goto need tag param")
            self.result = False
        
            
    def innerProcess(self): 
        if not self.result:
            return
        
        if "size" in self.params:
            self._size = int(self.params.get("size"))
            
        if "from" in self.params:
            self._from = self.params.get("from")
            
        if "tag" in self.params:
            self._tag = self.params.get("tag")
           
        with open(self._logfile,"r") as logfile:
            
            if not logfile:
                message = "logfile not exist"
            else:
        
                try:
                
                    if self._command == "pulllog":
                        self.command_pulllog(logfile)
                            
                    elif self._command == "mark" and self._tag:                  
                        self.command_mark()                      
                        
                    elif self._command == "goto" and self._tag:
                        self.command_goto()                             
                         
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    message = sys.exc_info()
                    self.send_response(400)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write("server process error")   
                    self.wfile.write(message)    
        
    def command_pulllog(self,logfile):
        filelength = os.stat(self._logfile).st_size
        index = 0
        

        with DraggerHttpHandler.indexLock:    
            if self._from in DraggerHttpHandler.fileIndexKeeper:
                index = DraggerHttpHandler.fileIndexKeeper.get(self._from)
            
            if index + self._size > filelength:
                self._size = filelength - index
               
            DraggerHttpHandler.fileIndexKeeper[self._from] = index + self._size
       
         
        
        logfile.seek(index)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        while self._size > 0:
            line = logfile.readline()
            self._size -= len(line)
            self.wfile.write(line)
            self.wfile.write(file.newlines)
                
        
    def command_mark(self): 
        index = -1
        
        with DraggerHttpHandler.indexLock: 
            if self._from in DraggerHttpHandler.fileIndexKeeper:
                index = DraggerHttpHandler.fileIndexKeeper.get(self._from)
                
        with DraggerHttpHandler.markLock:
            if index >= 0:
                markKey = self._from + "-" + self._tag
                DraggerHttpHandler.fileMarkKeeper[markKey] = index
            
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("mark success")
       
    def command_goto(self):
        index = -1
                    
        with DraggerHttpHandler.markLock:
            markKey = self._from + "-" + self._tag
            if markKey in DraggerHttpHandler.fileMarkKeeper:
                index = DraggerHttpHandler.fileMarkKeeper.get(markKey)
        
        with DraggerHttpHandler.indexLock:
            if self._from in DraggerHttpHandler.fileIndexKeeper:
                if index >= 0:
                    DraggerHttpHandler.fileIndexKeeper[self._from] = index
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("goto success") 

        