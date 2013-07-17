from bins import *
from math import ceil
import itertools


def first_fit(items, bins):
    """
    First fit heuristic:
        place an item in the bin with the
        smallest remaining space possible

    Bins might be empty or not
    """

    for i in items:
        bins.sort(key=lambda x: x.remaining, reverse=False)
        added = False
        for b in bins:
            if b.add(i):
                added = True
                break
        if not added:
            return False

    return True

def compute_min_bins(items, capacity):
    """
    Compute bound L2 a lower bound on the minimum number
    of bins with given capacity to fit the items

    Implementation based on Chapter 8, pp228-233, from:
    Knapsack problems: algorithms and computer implementations.
    Martello, Silvano, and Paolo Toth.
    John Wiley & Sons, Inc., 1990.
    """
    items.sort(reverse=True)
    j = 0
    for i in items:
        if 2*i.size <= capacity: break
        j += 1
    # Items[j-1] is the smallest item bigger than cap/2
    # Items[j] is the biggest item smaller than cap/2

    if j >= len(items):
        # All items are bigger than cap/2 - bound is tight
        return len(items)

    if j == 0:
        # All items are smaller than cap/2
        return int(ceil(float(sum(i.size for i in items))/capacity))

    cj12 = j-1       # |J1|+|J2|
    sj = 0
    for i in itertools.islice(items,j,len(items)):
        sj += i.size

    j1 = j
    tmp = capacity - items[j].size
    count = 0
    for i in itertools.islice(items,0,j):
        if i.size <= tmp:
            j1 = count
            break
        count += 1

    cj2 = j - j1
    sj2 = 0
    for i in itertools.islice(items,j1,j):
        sj2 += i.size

    j2 = j
    tmp = items[j2].size
    sj3 = tmp
    for i in itertools.islice(items,j2+1,len(items)):
        if i.size != tmp: break
        j2 += 1
        sj3 += tmp

    L2 = cj12
    first = True
    n = len(items)
    items.append(Item(0))
    while first or\
            (j2 < n and cj12 + ceil(float(sj+sj2)/capacity-cj2) > L2):
        first = False
        L2 = max(L2, cj12+ceil(float(sj3+sj2)/capacity-cj2))
        j2 += 1
        if j2 >= n: break
        tmp = items[j2].size
        sj3 += tmp
        for i in itertools.islice(items,j2+1,len(items)):
            if i.size != tmp: break
            j2 += 1
            sj3 += tmp
        tmp = capacity - tmp
        while j1 > 0 and items[j1-1].size <= tmp:
            j1 -= 1
            cj2 += 1
            sj2 += items[j1].size


    return int(L2)
