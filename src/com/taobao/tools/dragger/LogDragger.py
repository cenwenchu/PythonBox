'''
Created on 2011-9-28

@author: fangweng
'''

import sys,BaseHTTPServer
from DraggerHttpHandler import DraggerHttpHandler

if __name__ == '__main__':
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 7788
        
    server_address = ('',port)
    
    httpd = BaseHTTPServer.HTTPServer(server_address,DraggerHttpHandler)
    
    sa = httpd.socket.getsockname()
    
    print "Dragger Server on : ",sa[0],"port :",sa[1]," ..."
    
    httpd.serve_forever()