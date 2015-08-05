"""
run anatomize with given parameters
"""

# !/usr/bin/env python
# coding=utf-8

# by Qiyuan Gong
# qiyuangong@gmail.com

from anatomize import anatomize
from utils.read_data import read_data
import sys

if __name__ == '__main__':
    L = 10
    try:
        L = int(sys.argv[1])
    except (IndentationError, IndexError) as input_error:
        pass
    # read record
    RAW_DATA = read_data()
    # remove duplicate items
    print "Begin Anatomizer"
    RESULT = anatomize(RAW_DATA, L)
    print "No. groups in result=%d" % len(RESULT)
    print "Finish Anatomizer!!"
