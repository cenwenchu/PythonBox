'''
Created on 2011-10-18

@author: fangweng
'''
# -*- coding: utf-8 -*- 
import httplib,urllib

class SimpleTest(object):
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"} 
    
    def getTrade(self,session):
        params = urllib.urlencode({'fields':'orders.num_iid,orders.title,orders.price,buyer_message,end_time,seller_nick,buyer_nick,title,price,pic_path,num,tid,payment,total_fee,post_fee,receiver_name,receiver_state,receiver_city,receiver_district,receiver_address,receiver_mobile'})
        
        conn = httplib.HTTPConnection("localhost",7777)
        conn.request("GET","/2.0/trades.bought.json?debug=true&session=" + session+"&"+params, "", SimpleTest.headers)
        
        resp = conn.getresponse()
    
        data = resp.read()
    
        print data



def test():
    session = "41018330b956b2e7a91f1c5ce1dda551a7d9e2a1wJ0koaPt51020661"
    simpleTest = SimpleTest()
    
    simpleTest.getTrade(session)

if __name__ == '__main__':
    test()