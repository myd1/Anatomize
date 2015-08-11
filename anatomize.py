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
        """
        pop an element from SABucket
        """
        return self.member.pop()

    def __len__(self):
        """
        return number of records
        """
        return len(self.member)


class Group(object):
    """
    Group records to form Equivalent Class
    """

    def __init__(self):
        self.index = 0
        self.member = []
        self.checklist = set()

    def add_element(self, record, index):
        """
        add element pair (record, index) to Group
        """
        self.member.append(record[:])
        self.checklist.add(index)

    def check_index(self, index):
        """
        Check if index is in checklist
        """
        if index in self.checklist:
            return True
        return False

    def __len__(self):
        """
        return number of records
        """
        return len(self.member)


def build_SA_bucket(data):
    """
    build SA buckets and a heap sorted by number of records in bucket
    """
    buckets = {}
    bucket_heap = []
    # Assign SA into buckets
    for record in data:
        sa_value = record[-1]
        try:
            buckets[sa_value].append(record)
        except KeyError:
            buckets[sa_value] = [record]
    # random shuffle records in buckets
    # make pop random
    for key in buckets.keys():
        random.shuffle(buckets[key])
    # group stage
    # each round choose l largest buckets, then pop
    # an element from these buckets to form a group
    # We use heap to sort buckets.
    for i, bucketed_record in enumerate(buckets.values()):
        # push to heap reversely
        length = len(bucketed_record) * -1
        if length == 0:
            continue
        heapq.heappush(bucket_heap, (length, SABucket(bucketed_record, i)))
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
            (length, bucket) = heapq.heappop(bucket_heap)
            length_list.append(length)
            SAB_list.append(bucket)
        # pop an element from choosen buckets
        for i in range(L):
            bucket = SAB_list[i]
            length = length_list[i]
            newgroup.add_element(bucket.pop_element(), bucket.index)
            length += 1
            if length == 0:
                continue
            # push new tuple to heap
            heapq.heappush(bucket_heap, (length, bucket))
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
        (_, bucket) = heapq.heappop(bucket_heap)
        index = bucket.index
        candidate_set = []
        for group in groups:
            if group.check_index(index) is False:
                candidate_set.append(group)
        if len(candidate_set) == 0:
            suppress.extend(bucket.member[:])
        while bucket.member:
            candidate_len = len(candidate_set)
            if candidate_len == 0:
                break
            current_record = bucket.pop_element()
            group_index = random.randrange(candidate_len)
            group = candidate_set.pop(group_index)
            group.add_element(current_record, index)
        if len(bucket) >= 0:
            suppress.extend(bucket.member[:])
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
        for record in group.member:
            qi_part = record[:-1]
            qi_part.append(i)
            sa_part = [record[-1]]
            sa_part.insert(0, i)
            qi_table.append(qi_part)
            sa_table.append(sa_part)
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
