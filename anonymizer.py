#!/usr/bin/env python
#coding=utf-8

# by Qiyuan Gong
# qiyuangong@gmail.com

from anatomy import anatomy
from utils.read_data import read_data
import sys
# Poulis set k=25, m=2 as default!

if __name__ == '__main__':
    L = 10
    try:
        L = int(sys.argv[1])
    except:
        pass
    #read record
    data = read_data()
    # remove duplicate items
    print "Begin Partition"
    result = anatomy(data, L)
    print "Finish Partition!!"
