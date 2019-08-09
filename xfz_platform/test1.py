# -*- coding: utf-8 -*-#

"""
Name:           test1 
# Author:       wangyunfei
# Date:         2019-08-05
# Description:  
"""


def tribonacci(n):
    """
    :type n: int
    :rtype: int
    """
    from functools import reduce
    T = [0, 1, 1]
    if n < 3:
        return T[n]
    return reduce((lambda t, y: [t[1], t[2], sum(t)]), range(3, n + 1), T)[-1]


print(tribonacci(10))