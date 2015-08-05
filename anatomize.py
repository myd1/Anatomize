"""
Main module of Anatomize.
"""

# by Qiyuan Gong
# qiyuangong@gmail.com

# @INPROCEEDINGS{
#   author = {Xiao, Xiaokui and Tao, Yufei},
#   title = {Anatomy: simple and effective privacy preservation},
#   booktitle = {Proceedings of the 32nd international conference on Very large data
#     bases},
#   year = {2006},
#   series = {VLDB '06},
#   pages = {139--150},
#   publisher = {VLDB Endowment},
#   acmid = {1164141},
#   location = {Seoul, Korea},
#   numpages = {12}
# }

import random
import heapq


_DEBUG = False


class SABucket(object):
    """
    this class is used for bucketize
    in Anatomize. Each bucket indicate one SA value
    """

    def __init__(self, data, index):
        self.member = data[:]
        self.value = ""
        self.index = index

    def pop_element(self):
        """pop an element from SABucket
        """
        return self.member.pop()


class Group(object):
    """
    Group records to form Equivalent Class
    """

    def __init__(self):
        self.index = 0
        self.member = []
        self.checklist = set()

    def add_element(self, record, index):
        """add element pair (record, index) to Group
        """
        self.member.append(record[:])
        self.checklist.add(index)

    def check_index(self, index):
        """Check if index is in checklist
        """
        if index in self.checklist:
            return True
        return False


def anatomize(data, L):
    """
    only one SA is supported in anatomy.
    Separation grouped member into QIT and SAT
    Use heap to get l largest buckets
    L is the denote l in l-diversity.
    data is a list, i.e. [qi1,qi2,sa]
    """
    groups = []
    buckets = {}
    result = []
    suppress = []
    qi_table = []
    sa_table = []
    heap = []
    if _DEBUG:
        print '*' * 10
        print "Begin Anatomizer!"
    print "L=%d" % L
    # Assign SA into buckets
    for temp in data:
        list_temp = temp[-1]
        try:
            buckets[list_temp].append(temp)
        except:
            buckets[list_temp] = [temp]
    # group stage
    # each round choose l largest buckets, then pop
    # an element from these buckets to form a group
    # We use heap to sort buckets.
    for i, temp in enumerate(buckets.values()):
        # push to heap reversely
        pos = len(temp) * -1
        if pos == 0:
            continue
        heapq.heappush(heap, (pos, SABucket(temp, i)))
    while len(heap) >= L:
        newgroup = Group()
        length_list = []
        SAB_list = []
        # choose l largest buckets
        for i in range(L):
            (length, temp) = heapq.heappop(heap)
            length_list.append(length)
            SAB_list.append(temp)
        # pop an element from choosen buckets
        for i in range(L):
            temp = SAB_list[i]
            length = length_list[i]
            newgroup.add_element(temp.pop_element(), temp.index)
            length += 1
            if length == 0:
                continue
            # push new tuple to heap
            heapq.heappush(heap, (length, temp))
        groups.append(newgroup)
    # residue-assign stage
    # If the dataset is even distributed on SA, only one tuple will
    # remain in this stage. However, most dataset don't satisfy this
    # condition, so lots of records need to be re-assigned. In worse
    # case, some records cannot be assigned to any groups, which will
    # be suppressed (deleted).
    while len(heap):
        (length, temp) = heapq.heappop(heap)
        index = temp.index
        while temp.member:
            # pseudo-code in Xiao's paper use random in this step
            # Herein, I try groups in order. It's much faster.
            for group in groups:
                if group.check_index(index) is False:
                    group.add_element(temp.pop_element(), index)
                    break
            else:
                suppress.extend(temp.member[:])
                break
    # transform and print result
    for i, group in enumerate(groups):
        group.index = i
        result.append(group.member[:])
        # creat sa_table and qi_table
        for temp in group.member:
            qi_temp = temp[:-1]
            qi_temp.append(i)
            sa_temp = [temp[-1]]
            sa_temp.insert(0, i)
            qi_table.append(qi_temp)
            sa_table.append(sa_temp)
    if _DEBUG:
        print 'NO. of Suppress after anatomy = %d' % len(suppress)
        print 'NO. of groups = %d' % len(result)
        for i in range(len(qi_table)):
            print qi_table[i] + sa_table[i]
    return result
