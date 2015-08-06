"""
Main module of Anatomize.
"""

# implemented by Qiyuan Gong
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


def build_SA_bucket(data):
    """
    build SA buckets and a heap sorted by number of records in bucket
    """
    buckets = {}
    bucket_heap = []
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
        heapq.heappush(bucket_heap, (pos, SABucket(temp, i)))
    return buckets, bucket_heap


def assign_to_groups(buckets, bucket_heap, L):
    """
    assign records to groups.
    Each iterator pos 1 record from L largest bucket to form a group.
    """
    groups = []
    while len(bucket_heap) >= L:
        newgroup = Group()
        length_list = []
        SAB_list = []
        # choose l largest buckets
        for i in range(L):
            (length, temp) = heapq.heappop(bucket_heap)
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
            heapq.heappush(bucket_heap, (length, temp))
        groups.append(newgroup)
    return groups


def residue_assign(groups, bucket_heap):
    """
    residue-assign stage
    If the dataset is even distributed on SA, only one tuple will
    remain in this stage. However, most dataset don't satisfy this
    condition, so lots of records need to be re-assigned. In worse
    case, some records cannot be assigned to any groups, which will
    be suppressed (deleted).
    """
    suppress = []
    while len(bucket_heap):
        (_, temp) = heapq.heappop(bucket_heap)
        index = temp.index
        candidate_set = []
        for group in groups:
            if group.check_index(index) is False:
                candidate_set.append(group)
        if len(candidate_set) == 0:
            suppress.extend(temp.member[:])
        while temp.member:
            candidate_len = len(candidate_set)
            if candidate_len == 0:
                break
            current_record = temp.pop_element()
            group_index = random.randrange(candidate_len)
            group = candidate_set.pop(group_index)
            group.add_element(current_record, index)
        if len(temp.member) >= 0:
            suppress.extend(temp.member[:])
    return groups, suppress


def split_table(groups):
    """
    split table to qi_table, sa_table and grouped result
    qi_table contains qi and gid
    sa_table contains sa and gid
    result contains raw data grouped
    """
    qi_table = []
    sa_table = []
    result = []
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
    return qi_table, sa_table, result


def anatomize(data, L):
    """
    only one SA is supported in anatomy.
    Separation grouped member into QIT and SAT
    Use heap to get l largest buckets
    L is the denote l in l-diversity.
    data is a list, i.e. [qi1,qi2,sa]
    """
    if _DEBUG:
        print '*' * 10
        print "Begin Anatomizer!"
    print "L=%d" % L
    # build SA buckets
    buckets, bucket_heap = build_SA_bucket(data)
    # assign records to groups
    groups = assign_to_groups(buckets, bucket_heap, L)
    # handle residue records
    groups, suppress = residue_assign(groups, bucket_heap)
    # transform and print result
    qi_table, sa_table, result = split_table(groups)
    if _DEBUG:
        print 'NO. of Suppress after anatomy = %d' % len(suppress)
        print 'NO. of groups = %d' % len(result)
        for i in range(len(qi_table)):
            print qi_table[i] + sa_table[i]
    return result
