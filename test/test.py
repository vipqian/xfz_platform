# -*- coding: utf-8 -*-#

"""
Name:           test 
# Author:       wangyunfei
# Date:         2019-07-12
# Description:  
"""


import requests

url = 'http://127.0.0.1:8000/api/login/'

params = {
   'telephone': '1223',
   'password': '123',
   'remember': '1'
}

r = requests.post(url, data=params)

print(r.text)