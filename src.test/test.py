# -*- coding: utf-8 -*- 
import httplib,urllib

class HttpClientDemo(object):
    
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}   
    
    def addItem(self,session):
        
        params = urllib.urlencode({'post_fee':'5.00','express_fee':'15.00','ems_fee':'25.00','num':10,'price':'22.00','type':'fixed','stuff_status':'new','title':'贝因美 宝宝青菜营养肉酥 婴儿 儿童肉松','freight_payer':'buyer','location.city':'杭州','location.state':'浙江','cid':50018803,'desc':'<p><font color=\"#ff0000\"><span style=\"font-size: 16.0pt;font-family: 华文中宋;mso-ascii-font-family: 华文中宋;mso-fareast-font-family: 华文中宋;mso-hansi-font-family: 华文中宋;\"><strong>专为中国宝宝研制<\/strong><\/span><span style=\"font-size: 16.0pt;font-family: 华文中宋;mso-ascii-font-family: 华文中宋;mso-fareast-font-family: 华文中宋;mso-hansi-font-family: 华文中宋;\"><strong>特别适合<\/strong><\/span><span style=\"font-size: 16.0pt;font-family: 华文中宋;mso-ascii-font-family: 华文中宋;mso-fareast-font-family: 华文中宋;mso-hansi-font-family: 华文中宋;mso-fareast-language: zh-cn;\"><strong>6个月--6岁宝宝<\/strong><\/span><\/font><\/p>\n<li><font color=\"#000099\">适用对象：<em><strong>6-72<\/strong>个月婴儿<\/em> <\/font><\/li>\n<li><font color=\"#000099\">产品规格：115g <\/font><\/li>\n<li><font color=\"#000099\">产品标准：Q\/DWX 0001 <\/font><\/li>\n<li><font color=\"#000099\">保质期：十二个月 <\/font><\/li>\n<div>\n<h3><font color=\"#000099\">产品特点<\/font><\/h3>\n<p><font color=\"#000099\">贝因美宝宝菠菜营养肉酥精选优质鲜猪后腿精肉为原料，特别添加菠菜粉（含铁），含蛋白质、钙、铁、锌、B 族元素等多种人体必需的营养成分。产品采用先进设备和工艺技术精制而成，纤维细小，入口即化，易消化吸收，是宝宝理想的营养补充食品。<\/font><\/p><\/div>'})   
    
        conn = httplib.HTTPConnection("localhost",7777)
        conn.request("PUT","/2.0/item.json?debug=true&session=" + session, params, HttpClientDemo.headers)
        
        resp = conn.getresponse()
    
        data = resp.read()
    
        print data
        
        if (data and data.find("created") > 0 and data.find("iid") > 0):
            iid = data[data.index("iid")+6:data.index("num_iid")-3]
            return iid
        else:
            return None
        
    def getItem(self,iid,session):
        params = urllib.urlencode({'num_iid':iid,'fields':'post_fee,num,price,type,stuff_status,title,desc,location.state,location.city,approve_status,cid,props,freight_payer,valid_thru'})
        
        conn = httplib.HTTPConnection("localhost",7777)
        conn.request("GET","/2.0/item.json?debug=true&session=" + session+"&"+params, "", HttpClientDemo.headers)
        
        resp = conn.getresponse()
    
        data = resp.read()
    
        print data
        
    def updateItem(self,iid,session):
        params = urllib.urlencode({'num_iid':iid,'post_fee':'6.00'})
        
        conn = httplib.HTTPConnection("localhost",7777)
        conn.request("POST","/2.0/item.json?debug=true&session=" + session, params, HttpClientDemo.headers)
        
        resp = conn.getresponse()
    
        data = resp.read()
    
        print data
        
    def deleteItem(self,iid,session):
        params = urllib.urlencode({'num_iid':iid})
       
        conn = httplib.HTTPConnection("localhost",7777)
        conn.request("DELETE","/2.0/item.json?debug=true&session=" + session, params, HttpClientDemo.headers)
        
        resp = conn.getresponse()
    
        data = resp.read()
    
        print data
        
       
def test():
    session = "41018330b956b2e7a91f1c5ce1dda551a7d9e2a1wJ0koaPt51020661"
    clientDemo = HttpClientDemo()
    
    
    iid = clientDemo.addItem(session)
        
    if (iid):
        clientDemo.getItem(iid,session)
        clientDemo.updateItem(iid,session)
        clientDemo.getItem(iid, session)
        clientDemo.deleteItem(iid, session)
        
    
    
if (__name__  == "__main__"):
    test()
    

