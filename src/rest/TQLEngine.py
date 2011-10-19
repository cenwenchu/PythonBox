'''
Created on 2011-10-19

@author: fangweng
'''
import urllib

class TQLEngine(object):
    
    def process(self,url,method,header):
        
        desturl = "http://gw.api.taobao.com/router/rest?"
        
        paramsStr = url.split(" ")[1]
        if (paramsStr.find("?") > 0):
            paramsStr = paramsStr[paramsStr.index("?")+1:]
            
        params = dict()
        ps = paramsStr.split("&")
        
        for p in ps:
            params[p[:p.index("=")]] = p[p.index("=")+1:]
            
        for p in params.keys():
            if (p == "tql"):
                ql = urllib.unquote_plus(params[p])
                qlparts = ql.split(" ")
                fields = qlparts[1]
                apiname = qlparts[3]
                condition = qlparts[5:]
                
                desturl += "method=taobao." + apiname + ".get&fields=" + fields + "&"
                
                for c in condition:
                    if (c != "and" and c.find("=") > 0):
                        desturl += c + "&"
                
            else:
                desturl += p + "=" + params[p] + "&"
                
        if (desturl.endswith("&")):
            desturl = desturl[:len(desturl)-1]
        
        return desturl
            
            
            

if (__name__ == "__main__"):
    str = "GET /tql?tql=select+aa,bb,cc+from+user+where+nick=cenwenchu&session=41019340b956b2e7a91f1c5ce1dda551a7d9e2a15eflTqx4N1020661 HTTP/1.1"
    
    tqlEngine = TQLEngine()
    desturl = tqlEngine.process(str, None, None)
    print desturl
    
