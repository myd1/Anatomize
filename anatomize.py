import random
import heapq

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


_DEBUG = False


class SABucket(object):
    """this class is used for bucketize
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
    GT = []
    ST = []
    h = []
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
        heapq.heappush(h, (pos, SABucket(temp, i)))
    while len(h) >= L:
        newgroup = Group()
        length_list = []
        SAB_list = []
        # choose l largest buckets
        for i in range(L):
            (length, temp) = heapq.heappop(h)
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
            heapq.heappush(h, (length, temp))
        groups.append(newgroup)
    # residue-assign stage
    # If the dataset is even distributed on SA, only one tuple will
    # remain in this stage. However, most dataset don't satisfy this
    # condition, so lots of records need to be re-assigned. In worse
    # case, some records cannot be assigned to any groups, which will
    # be suppressed (deleted).
    while len(h):
        (length, temp) = heapq.heappop(h)
        index = temp.index
        while temp.member:
            # pseudo-code in Xiao's paper use random in this step
            # Herein, I try groups in order. It's much faster.
            for g in groups:
                if g.check_index(index) is False:
                    g.add_element(temp.pop_element(), index)
                    break
            else:
                suppress.extend(temp.member[:])
                break
    # transform and print result
    for i, t in enumerate(groups):
        t.index = i
        result.append(t.member[:])
        # creat ST and GT
        for temp in t.member:
            GT_temp = temp[:-1]
            GT_temp.append(i)
            SA_temp = [temp[-1]]
            SA_temp.insert(0, i)
            GT.append(GT_temp)
            ST.append(SA_temp)
    if _DEBUG:
        print 'NO. of Suppress after anatomy = %d' % len(suppress)
        print 'NO. of groups = %d' % len(result)
        for i in range(len(GT)):
            print GT[i] + ST[i]
    return result
