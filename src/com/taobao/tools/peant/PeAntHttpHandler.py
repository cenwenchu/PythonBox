'''
Created on 2011-9-25

@author: fangweng
'''

import BaseHTTPServer,time
from PeWorker import PeWorker


class PeAntHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        line = self.requestline.split(" ")[1]
        self.innerProcess(line[line.find("?")+1:]) 
            
        
            
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))    
        p_body = self.rfile.read(length)
        self.innerProcess(p_body)    
    
    def innerProcess(self,p_body):
        
        worker = PeWorker('PeWorkder' + str(time.time()),p_body)
        worker.setDaemon(True)
        worker.start()    
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("ok")
        

        