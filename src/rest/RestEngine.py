'''
Created on 2011-9-29

@author: fangweng
'''


import threading,xml.etree.ElementTree as et
from RestMappingElement import APIMapping,Rule

class RestEngine(object):
    '''
    load rest_def config file, format url to params ,format params to url 
    '''
    handlerPool = dict()
    lock = threading.Lock()


    def __init__(self,conf):
        
        self.conf = conf
        
        self.mapping = dict()
        
        with open(self.conf,"r") as cfile:
            self.parseConfig(cfile)
            
            
    def parseConfig(self,cfile):
        tree = et.parse(cfile)
        mappingList = tree.getroot().findall("api_mapping")
        
        for parent in mappingList:
            
            host = parent.get("host") 
            
            if (parent.get("desthost")):
                desthost = parent.get("desthost")
            else:
                desthost = host
            
            apiMapping = APIMapping(host,desthost)
            self.mapping[host] = apiMapping
            
            for child in parent:
                if (child.tag == "rule"):
                    
                    paramName = ""
                    header = ""
                    uriIndex = ""
                    mappingClass = ""
                    
                    if (child.get("paramName")):
                        paramName = child.get("paramName")
                    else:
                        continue
                    
                    if (child.get("header")):
                        header = child.get("header")
                        
                    if (child.get("uriIndex")):
                        uriIndex = child.get("uriIndex")
                        
                    if (child.get("mappingClass")):
                        mappingClass = child.get("mappingClass")
                    
                    rule = Rule(paramName,header,uriIndex,mappingClass)
                    apiMapping.rules.append(rule)           
            
    
    
    def process(self,url,method,header):
        host = header.get("HOST")
        params = dict()
        destUrl = url
        
        if host in self.mapping or "*" in self.mapping:
            
            if host in self.mapping:
                apiMapping = self.mapping.get(host)
            else:
                apiMapping = self.mapping.get("*")
                   
            print url 
            if (url.find("?") > 0):    
                urlbricks = url[:url.index("?")].split(" ")[1].split("/")[1:]
            else:
                urlbricks = url.split(" ")[1].split("/")[1:]
            
            for rule in apiMapping.rules:
                if (rule.header):
                    if (rule.header in header):
                        params[rule.paramName] = header.get(rule.header)
                elif (rule.uriIndex):
                    
                    if(int(rule.uriIndex) > len(urlbricks)):
                        continue
                    
                    if(rule.mappingClass):
                        
                        mappingObj = None
                        
                        with RestEngine.lock:
                            if rule.mappingClass in RestEngine.handlerPool:
                                mappingObj = RestEngine.handlerPool.get(rule.mappingClass)
                                
                        if  not mappingObj:
                            m = __import__(rule.mappingClass[:rule.mappingClass.index(".")],globals(),locals(),[rule.mappingClass[rule.mappingClass.index(".")+1:]])
                            mappingClass = getattr(m, rule.mappingClass[rule.mappingClass.index(".")+1:])
                            mappingObj = mappingClass()
                            RestEngine.handlerPool[rule.mappingClass] = mappingObj
                            
                        params[rule.paramName] = mappingObj.do_map(method,urlbricks[int(rule.uriIndex)-1])         
                    else:
                        params[rule.paramName] = urlbricks[int(rule.uriIndex)-1]
                        
            
            if (url.find("?") > 0):  
                destUrl = "" + apiMapping.desthost + url[url.index("?"):].split(" ")[0]
                firstParam = False
            else:
                destUrl = "" + apiMapping.desthost + "?"
                firstParam = True
            
            for p in params:
                if (firstParam):
                    destUrl += p + "=" + params.get(p)
                    firstParam = False
                else:
                    destUrl += "&" + p + "=" + params.get(p)
                
        return destUrl
            
        
        
def test():
    engine = RestEngine("/Users/apple/Documents/workspace/PythonBox/src.test/rest_def.xml")
    print engine
    
if( __name__ == "__main__"):
    test()
        
        
        