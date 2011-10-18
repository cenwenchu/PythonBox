'''
Created on 2011-9-29

@author: fangweng
'''

import BaseHTTPServer,httplib,urllib,datetime,md5,urllib2,cgi,copy
from RestEngine import RestEngine

class RestHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    conf = "rest_def.xml"
    restEngine = RestEngine(conf)
    
    def do_GET(self):
        
        if (self.requestline.find("favicon.ico") > 0):
            return
        
        if (self.requestline.find("/getcode") > 0):
            self.auth(self.requestline)  
        else:
            url = RestHttpHandler.restEngine.process(self.requestline, self.command,self.headers)
            self.do_proxy(url)   
        
            
    def do_POST(self):
        if (self.requestline.find("favicon.ico") > 0):
            return
        
        if (self.requestline.find("/getcode") > 0):
            self.auth(self.requestline)  
        else:
            url = RestHttpHandler.restEngine.process(self.requestline, self.command,self.headers)
            self.getParamsFromPOSTBody()
            self.do_proxy(url) 
                
    def do_DELETE(self):
        self.do_POST()
        
    def do_PUT(self):    
        self.do_POST()
            
    def getParamsFromPOSTBody(self):
        
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        
        self.bparams = dict()
        
        for field in form.keys():
            field_item = form[field]
            if not field_item.file:
                self.bparams[field] = field_item.value
            
        

    def auth(self,url):
        desturl = url[url.index("?")+1:]    
        params = desturl.split(" ")[0].split("&")
        
        state = None
        
        for p in params:
            if p.startswith("code="):
                authcode = p[5:]
            if p.startswith("state="):
                state = p[6:]
        
        if (state):
            if (state == "sina"):
                desturl = "grant_type=authorization_code&code=" + authcode + \
                    "&redirect_uri=http://www.mashupshow.com/showcode&client_secret=3a69bb60ed46d0ceab5f0457657ac0f9&client_id=845619194"
            if (state == "taobao"):
                desturl = "grant_type=authorization_code&code=" + authcode + \
                    "&redirect_uri=http://www.mashupshow.com/showcode&client_secret=e5b6de2da468af71f530337d2851c944&client_id=12131536"
        else:
            desturl = "grant_type=authorization_code&code=" + authcode + \
                "&redirect_uri=http://www.mashupshow.com/showcode&client_secret=e5b6de2da468af71f530337d2851c944&client_id=12131536"
        
        params = desturl.split("&")
        paraDict = dict()
        
        for p in params:
            paraDict[p[:p.index("=")]] = p[p.index("=")+1:]
                   
        params = urllib.urlencode(paraDict)
        
        print params
        
        if (state and state == "sina"):
            conn = httplib.HTTPSConnection("api.weibo.com")
            conn.request("POST","/oauth2/access_token?"+params, params, dict(self.headers))
        else:
            conn = httplib.HTTPSConnection("oauth.taobao.com")
            conn.request("POST","/token?"+params, params, dict(self.headers))
            
        resp = conn.getresponse()
            
        self.send_response(resp.status)
        
        for m in resp.getheaders():
            if (m[0] == "content-type"):
                self.send_header("content-type", "text/plain")
            else:
                self.send_header(m[0],m[1])
            
        self.end_headers()    
        
        
        data = resp.read()
        while data :
            print data
            self.wfile.write(data)
            data = resp.read()
               
        conn.close()
        
        

    def sign(self,paraDict,secretCode):
        
        paramStr = secretCode
        
        for key in sorted(paraDict.iterkeys()):
            paramStr += key + paraDict[key]

        paramStr += secretCode
        
        return md5.md5(paramStr).hexdigest().upper()
        
    
    def do_proxy(self,url):
        command = self.command
        host = url[:url.index("?")]
        port = 80
        desturl = url[url.index("?")+1:]
        
        if (url.startswith("http://")):
            context = url[7:]
            if ("/" in context and "?" in context):
                context = context[context.index("/"):context.index("?")]
        else:
            context = url[context.index("/"):context.index("?")]
        
        params = desturl.split("&")
        paraDict = dict()
        
        for p in params:
            if p <> "":
                paraDict[p[:p.index("=")]] = urllib2.unquote(p[p.index("=")+1:]).decode("utf-8")
        
        #add default params  appkey=12241435   secretcode=d8b819caa2294732ef5e4a7525123e2b
        if ("app_key" not in paraDict):
            paraDict["app_key"] = "12131536"
            #paraDict["app_key"] = "4272"
            
        if ("timestamp" not in paraDict):
            paraDict["timestamp"] = str(datetime.datetime.now())
            paraDict["timestamp"] = paraDict["timestamp"][:paraDict["timestamp"].index(".")]
            
        if ("sign" not in paraDict):
            paraDict["sign_method"] = "md5"
            secretCode = "e5b6de2da468af71f530337d2851c944"
            #secretCode = "0ebbcccfee18d7ad1aebc5b135ffa906"
            if (command == "GET"):
                paraDict["sign"] = self.sign(paraDict,secretCode)
            else:
                tmpDict = copy.deepcopy(paraDict)
                
                for key in self.bparams.iterkeys():
                    tmpDict[key] = self.bparams[key]
                        
                paraDict["sign"] = self.sign(tmpDict,secretCode)
            
        
        if (host.startswith("http://")):
            host = host[host.startswith("http://") + len("http://") - 1:]
        
        if "/" in host:
            tmp = host[:host.index("/")]
            if (":" in tmp):
                host = tmp[:tmp.index(":")]
                port = int(tmp[tmp.index(":")+1:])
            else:
                host = tmp
                port = 80
            
        desturl = urllib.urlencode(paraDict)
            
        if (command != "GET"):
            params = urllib.urlencode(self.bparams)
            
        
        if (context):
            desturl = context + "?" + desturl
        else:
            desturl = "?" + desturl
        
          
        if (command == "PUT" or command == "DELETE"):
            command = "POST"
            
        print desturl
                   
        
        conn = httplib.HTTPConnection(host,port)
        
        if (command == "GET"):
            conn.request(command,desturl, None, dict(self.headers))
        else:
            conn.request(command,desturl, params, dict(self.headers))
        
        resp = conn.getresponse()
            
        self.send_response(resp.status)
        
        for m in resp.getheaders():
            if (m[0] == "top-innerip" or m[0] == "content-type" or m[0] == "date"):
                self.send_header(m[0],m[1])
           
        self.end_headers()    
        
        
        data = resp.read()
        
        print data
        
        while data :
            self.wfile.write(data)
            data = resp.read()
               
        conn.close()