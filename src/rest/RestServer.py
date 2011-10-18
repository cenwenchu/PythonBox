'''
Created on 2011-9-30

@author: fangweng
'''

import BaseHTTPServer,sys
from RestHttpHandler import RestHttpHandler

if __name__ == '__main__':
    
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 7777
        
    server_address = ('',port)
    
    httpd = BaseHTTPServer.HTTPServer(server_address,RestHttpHandler)
    
    sa = httpd.socket.getsockname()
    
    print "REST Server on : ",sa[0],"port :",sa[1]," ..."
    
    httpd.serve_forever()
