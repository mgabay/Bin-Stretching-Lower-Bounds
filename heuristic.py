##########################################################################
# Copyright or © or Copr. Michaël Gabay (2013)
#
# michael [dot] gabay [at] g-scop.grenoble-inp.fr
#
# This software is a computer program whose purpose is to be
# a proof of concept on using game theoretical approaches to prove
# lower bounds on online packing and scheduling problems.
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
##########################################################################

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
