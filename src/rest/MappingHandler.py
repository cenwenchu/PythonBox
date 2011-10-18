'''
Created on 2011-9-29

@author: fangweng
'''

import threading,sys
from RestMappingElement import RestSuffix

class RestMappingHandler(object):
    
    def do_map(self,httpMethod,source):
        pass


class FormatMappingHandler(RestMappingHandler):   
    def do_map(self,httpMethod,source):
        f = source[source.rindex(".")+1:] 
        return f


class APINameMappingHandler(RestMappingHandler):
    
    apis = dict()
    lock = threading.Lock()
    loadCompleted = False
    
    def __init__(self):
        if APINameMappingHandler.loadCompleted:
            return
        
        with APINameMappingHandler.lock:
            with open("api.def","r") as apifile:
                for line in apifile:
                    
                    try:
                    
                        if ("\n" in line):
                            line = line[:line.index("\n")]
                            
                        if (line.endswith(".get")):
                            self.createRestApi("GET",line)
                            continue
                            
                        if (line.endswith(".delete")):
                            self.createRestApi("DELETE",line)
                            continue
                            
                        if (line.endswith(".add")
                                or  line.endswith(".upload") or line.endswith(".publish") or line.endswith(".create")):
                            self.createRestApi("PUT",line)
                            continue
                                
                        if (line.endswith(".update") or line.endswith(".set")):
                            self.createRestApi("POST",line)
                            continue
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        print line
                        
                APINameMappingHandler.loadCompleted = True
     
    def createRestApi(self,method,line):
        suffix = line[line.rindex(".")+1:]   
        restSuffix = RestSuffix(method,suffix,line)
        
        if (method + line[line.index(".")+1:line.rindex(".")]) in APINameMappingHandler.apis:
            print "duplicate define : " + APINameMappingHandler.apis[method + line[line.index(".")+1:line.rindex(".")]].apiName + " , " + line
                
                            
        APINameMappingHandler.apis[method + line[line.index(".")+1:line.rindex(".")]] = restSuffix       
                      
    
    def do_map(self,httpMethod,source):
        if not APINameMappingHandler.loadCompleted:
            return source
        
        source = source[:source.rindex(".")]
        
        if (httpMethod.upper() + source) in APINameMappingHandler.apis:
            restSuffix = APINameMappingHandler.apis.get(httpMethod.upper() + source)
            source = "taobao." + source + "." + restSuffix.suffix
            
            
        return source
    
    
def unitTest():
    apiNameMapppingHandler = APINameMappingHandler()
    formatMappingHandler = FormatMappingHandler()
    
    apis = dict({"POST:shop":"taobao.shop.update","PUT:refund.message":"taobao.refund.message.add","GET:ju.items":"taobao.ju.items.get"
              ,"POST:taobao.promotion.coupon.send":"taobao.promotion.coupon.send","GET:taobao.jipiao.orders.searchbyuser":"taobao.jipiao.orders.searchbyuser",
              "PUT:product.img":"taobao.product.img.upload","POST:crm.rule.group":"taobao.crm.rule.group.set"})
    
    formater = "user.json"
    
    print formatMappingHandler.do_map("GET", formater)
    
    for api in apis:
        if (apiNameMapppingHandler.do_map(api.split(":")[0],api.split(":")[1]) <> apis.get(api)):
            print api + " error !"
        
          
if (__name__ == "__main__"):
    unitTest()


        

