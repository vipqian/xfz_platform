# -*- coding: utf-8 -*-#

"""
Name:           send_telephone_code 
# Author:       wangyunfei
# Date:         2019-05-09
# Description:  
"""

import requests

def sms_captcha_sender(mobile, captcha):

    url = 'http://v.juhe.cn/sms/send?'
    params = {
        'mobile': mobile,
        'tpl_id': '127598',
        'tpl_value': '#code#=%s' % captcha,
        'key': 'b7f6e51b7601629d1461b0ca9cc78ae5',
    }

    r = requests.get(url, params=params)
    if r.json()['error_code'] == 0:
        return True
    else:
        return False

