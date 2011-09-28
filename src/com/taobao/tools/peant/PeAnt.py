'''
Created on 2011-9-27

@author: fangweng
'''

import sys,BaseHTTPServer

from PeAntHttpHandler import PeAntHttpHandler

if __name__ == '__main__':
    
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8080
        
    server_address = ('',port)
    
    httpd = BaseHTTPServer.HTTPServer(server_address,PeAntHttpHandler)
    
    sa = httpd.socket.getsockname()
    
    print "PEAnt Server on : ",sa[0],"port :",sa[1]," ..."
    
    httpd.serve_forever()
        