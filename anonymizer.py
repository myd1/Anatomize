#!/usr/bin/env python
# coding=utf-8

# by Qiyuan Gong
# qiyuangong@gmail.com

from anatomizer import anatomizer
from utils.read_data import read_data
import sys
# Poulis set k=25, m=2 as default!

if __name__ == '__main__':
    L = 10
    try:
        L = int(sys.argv[1])
    except:
        pass
    # read record
    data = read_data()
    # remove duplicate items
    print "Begin Anatomizer"
    result = anatomizer(data, L)
    print "No. groups in result=%d" % len(result)
    print "Finish Anatomizer!!"
