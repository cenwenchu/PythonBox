'''
Created on 2011-9-29

@author: fangweng
'''

class Rule(object):
    def __init__(self,paramName,header,uriIndex,mappingClass):  
        self.paramName = paramName
        self.header = header
        self.uriIndex = uriIndex
        self.mappingClass = mappingClass      

class APIMapping(object):
    
    def __init__(self,host,desthost):
        self.host = host
        self.desthost = desthost
        self.rules = []
        
        
class RestSuffix(object):
    def __init__(self,httpMethod,suffix,apiName):
        self.apiName = apiName
        self.httpMethod = httpMethod
        self.suffix = suffix
