'''
Created on 2011-9-26

@author: fangweng
'''

import httplib,urllib

class HttpClientDemo(object):
    
    def postTest(self):
        
#        _myurl = 'http://localhost:8080?content=%23%21bin%2Fsh%0D%0Auseradd+zhenzi%0D%0Aecho+%22success%22&id=1&timestamp=1234567890&type=2&proxyIp=10.13.105.156:8080'
#                   
#        f = urllib.urlopen(_myurl)
#        
#        print f
        

        params = urllib.urlencode({'id':'1','timestamp':'1234567890','type':'2','content':'ls /Users/apple','proxyIp':'10.13.105.156:8080'})
        headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
    
        try:
        
            conn = httplib.HTTPConnection("localhost","8080")
            conn.connect()
            conn.request("POST",'', params, headers)
        
            response = conn.getresponse()
        
            data = response.read()
        
            print data
        finally:
           conn.close()
       
       
       
def test():
    clientDemo = HttpClientDemo()
    clientDemo.postTest()
    
    
if (__name__  == "__main__"):
    test()
    

