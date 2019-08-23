# -*- coding: utf-8 -*-#

"""
Name:           test 
# Author:       wangyunfei
# Date:         2019-08-23
# Description:  
"""



def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"] # python3
    #return ["Hello World"] # python2