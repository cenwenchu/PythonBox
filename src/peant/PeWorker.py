'''
Created on 2011-9-26

@author: fangweng
'''
import threading,subprocess,urllib,os

class PeWorker(threading.Thread):
    
    def __init__(self,name,content):
        threading.Thread.__init__(self,name=name)
        self.content = content
        
        
    def run(self):
        params = self.content.split("&")
        
        for param in params:
            if param.startswith("id"):
                self.p_id = param[param.index("=")+1:]
                continue
            
            if param.startswith("timestamp"):
                self.p_timestamp = param[param.index("=")+1:]
                continue
            
            if param.startswith("type"):
                self.p_type = param[param.index("=")+1:]
                continue
            
            if param.startswith("proxyIp"):
                self.p_proxyIp = param[param.index("=")+1:]
                continue
            
            if param.startswith("content"):
                self.p_content = param[param.index("=")+1:]
                continue
            
            if param.startswith("sign"):
                self.p_sign = param[param.index("=")+1:]
                continue
        
        if self.p_content and self.p_id and self.p_proxyIp:
            filename = '/tmp/' + self.p_id + self.p_proxyIp + self.p_timestamp + self.p_type
            
            with open (filename,'w') as commandfile:
                commandfile.write(urllib.unquote_plus(self.p_content))
            
            
            f = subprocess.Popen(('sh',filename), stdout=subprocess.PIPE).stdout 
            
            self.result = ''
            
            for eachLine in f:
                self.result += eachLine.strip()
           
            f.close()
            
            os.remove(filename)
        
        self.reportTaskResult()
        
    
    def reportTaskResult(self):
        params = urllib.urlencode({'id':self.p_id,'result':self.result})
        reporturl = "http://{0}/isvhosting/feedback?{1}".format(self.p_proxyIp,params)
        print reporturl
        
        f = urllib.urlopen(reporturl)
        
        print f
