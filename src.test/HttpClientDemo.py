'''
Created on 2011-9-26

@author: fangweng
'''

import httplib,urllib

# -*- coding: utf-8 -*- 

class HttpClientDemo(object):
    
    def postTest(self):
        
#        _myurl = 'http://localhost:8080?content=%23%21bin%2Fsh%0D%0Auseradd+zhenzi%0D%0Aecho+%22success%22&id=1&timestamp=1234567890&type=2&proxyIp=10.13.105.156:8080'
#                   
#        f = urllib.urlopen(_myurl)
#        
#        print f
        

#        params = urllib.urlencode({'id':'1','timestamp':'1234567890','type':'2','content':'ls /Users/apple','proxyIp':'10.13.105.156:8080'})
#        headers = {"Content-type": "application/x-www-form-urlencoded",
#            "Accept": "text/plain"}
#    
#        try:
#        
#            conn = httplib.HTTPConnection("localhost","8080")
#            conn.connect()
#            conn.request("POST",'', params, headers)
#        
#            response = conn.getresponse()
#        
#            data = response.read()
#        
#            print data
#        finally:
#           conn.close()
           
        params= u"你好"
        
        print params
        
        #params = urllib.urlencode({'num':10,'price':'22.00','type':'fixed','stuff_status':'new','title':'贝因美 宝宝青菜营养肉酥 婴儿 儿童肉松','freight_payer':'buyer','location.city':'杭州','location.state':'浙江','cid':50018803,'desc':'<p><font color=\"#ff0000\"><span style=\"font-size: 16.0pt;font-family: 华文中宋;mso-ascii-font-family: 华文中宋;mso-fareast-font-family: 华文中宋;mso-hansi-font-family: 华文中宋;\"><strong>专为中国宝宝研制<\/strong><\/span><span style=\"font-size: 16.0pt;font-family: 华文中宋;mso-ascii-font-family: 华文中宋;mso-fareast-font-family: 华文中宋;mso-hansi-font-family: 华文中宋;\"><strong>特别适合<\/strong><\/span><span style=\"font-size: 16.0pt;font-family: 华文中宋;mso-ascii-font-family: 华文中宋;mso-fareast-font-family: 华文中宋;mso-hansi-font-family: 华文中宋;mso-fareast-language: zh-cn;\"><strong>6个月--6岁宝宝<\/strong><\/span><\/font><\/p>\n<li><font color=\"#000099\">适用对象：<em><strong>6-72<\/strong>个月婴儿<\/em> <\/font><\/li>\n<li><font color=\"#000099\">产品规格：115g <\/font><\/li>\n<li><font color=\"#000099\">产品标准：Q\/DWX 0001 <\/font><\/li>\n<li><font color=\"#000099\">保质期：十二个月 <\/font><\/li>\n<div>\n<h3><font color=\"#000099\">产品特点<\/font><\/h3>\n<p><font color=\"#000099\">贝因美宝宝菠菜营养肉酥精选优质鲜猪后腿精肉为原料，特别添加菠菜粉（含铁），含蛋白质、钙、铁、锌、B 族元素等多种人体必需的营养成分。产品采用先进设备和工艺技术精制而成，纤维细小，入口即化，易消化吸收，是宝宝理想的营养补充食品。<\/font><\/p><\/div>'})
#        headers = {"Content-type": "application/x-www-form-urlencoded",
#            "Accept": "text/plain"}     
#    
#        try:
#        
#            conn = httplib.HTTPConnection("localhost","7777")
#            conn.connect()
#            conn.request("PUT",'/2.0/item.json', params, headers)
#        
#            response = conn.getresponse()
#        
#            data = response.read()
#        
#            print data
#        finally:
#           conn.close()   
       
       
       
def test():
    clientDemo = HttpClientDemo()
    clientDemo.postTest()
    
    
if (__name__  == "__main__"):
    test()
    

