'''
=======================
Author:李浩
时间：2020/2/25:10:49
Email:lihaolh_v@didichuxing.com
=======================
'''
import requests

class SendRequest(object):
    def __init__(self):
        self.session = requests.session()

    def send_request(self,url,method,headers = None,data = None,json =None,files = None,params = None):
        method = method.lower()

        if method == "get":
            response = self.session.get(url=url,headers=headers,params=params)
        elif method == "post":
            response = self.session.post(url=url,headers=headers,data=data,json=json,files=files)
        elif method == "patch":
            response = self.session.patch(url=url,headers=headers,data=data,json=json,files=files)
        return response

