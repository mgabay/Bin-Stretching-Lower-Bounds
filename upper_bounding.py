"""
A Branch-and-Bound approach, used to simulate an adversary for the online
bin stretching problem. The opponent decides which is the next item based on
the decisions taken by the decision maker (a deterministic algorithm).
The aim is to maximize the score against any deterministic algorithm.
That is: maximize alpha s.t. there exist some opponent choices that forces
any deterministic algorith to fill items into bins with a stretching factor
at least 1+alpha.

Remark: if memory is an issue, search for "MEMORY" comments and you will
    be able to spare some unnecessary used space
"""

import time
from bins import *
from bpsolver import *
import argparse
import binascii

# TODO:
#   Solution tracking, format: (configuration, item, solutions)
#       (recursive format: in given configuration, give this item
#       then chose solution corresponding to the new configuration)

IPSolver="GLPK"


################## Engine ####################

def run(weights, num_bins, capacity=1, lower_bound=-1):
    """Finds the best feasible upper bound within given limits

    Keyword arguments:
    weights -- the set of allowed weights
    num_bins -- number of bins
    capacity -- bins capacity

    Return maximal capacity required
    (stretching factor = ret / capacity)
    """
    bins = bin_factory(num_bins, capacity)

    # Keep only feasible weights
    ws = []
    for w in weights:
        if w <= capacity:
            ws.append(w)

    # Sort items by decreasing order of their weights
    ws.sort(reverse=True)

    d = {}
    if lower_bound == -1:
        lower_bound = capacity
    val = branch(ws, bins, num_bins*capacity, lower_bound, 2*capacity, d)

    """ Memory profiling
    from guppy import hpy
    h = hpy()
    print h.heap()
    """

    return val


ttime = 0
def is_feasible_instance(bins, item):
    """
    Return true iff there is a feasible solution
    for the bin packing problem with len(bins) bins,
    their items, plus the additionnal given item.

    Bins capacity are assumed to be all the same.
    """
    if item.size == 0:
        raise NameError('Adding a null sized item!')
    if not bins:
        return False

    items = [i for b in bins for i in b.items]
    items.append(item)

    global ttime
    t = time.time()
    r = is_feasible(items, len(bins), bins[0].capacity, IPSolver)
    ttime += time.time() - t
    return r


####### Memoization #######
def make_key(bins):
    l = []
    d = {}
    for b in bins:
        l.append(b.remaining)
        for i in b.items:
            s = i.size
            if s not in d: d[s] = 1
            else: d[s] += 1
    l.sort()
    # MEMORY: spare some memory by removing the following line:
    l.append(-1)
    # separate bins from items / use less memory than making a list of tuples...
    # not required here since the number of bins is fixed
    for i, j in d.iteritems():
        l.append(i)
        l.append(j)

    return binascii.rlecode_hqx(' '.join(str(i) for i in l))
    #return tuple(l)


def recall(memo, t, lower_bound, upper_bound):
    if not t in memo:
        return False
    lb, ub, val = memo[t]
    if val >= ub and ub < upper_bound:
        return False
    if val <= lb and lb > lower_bound:
        return False
    return val


def solve(memo, bins, lower_bound, upper_bound, rem_cap, weights):
    t = make_key(bins)
    ret = recall(memo, t, lower_bound, upper_bound)
    if ret: return ret
    ret = branch(weights, bins, rem_cap, lower_bound, upper_bound, memo)
    memo[t] = (lower_bound, upper_bound, ret)
    return ret


####### End Memoization #######

def branch(weights, bins, rem_cap, lower_bound, upper_bound, memo={}):
    """
    Branching: Finds the best feasible upper bound within given limits
    Depth first search exploration

    Keyword arguments:
    weights -- the set of allowed weights
    bins -- the bins
    rem_cap -- total remaining capacity in bins
    lower_bound -- lower bound on the stretched capacity.
        We are aiming at improving it.
    upper_bound -- upper bound on the stretched capacity.
        It is no use to go beyond the upper bound since the results
        will be neglected by some other branches.

    Return maximal stretching factor
    """
    if not bins:
        raise NameError('Branching to pack items in... no bins!')
    assert rem_cap >= 0
    if lower_bound >= upper_bound:
        return upper_bound

    # Smallest and largest used capacities
    u = bins[0].used()
    min_bin = u
    max_bin = u
    for b in bins:
        u = b.used()
        max_bin = max(u, max_bin)
        min_bin = min(u, min_bin)
    lower_bound = max(max_bin, lower_bound)

    if max_bin >= upper_bound:
        # fathom branch:  we have stretched enough already
        return upper_bound
    """
    if max_bin + rem_cap <= lower_bound:
        # useless branch
        return lower_bound
    max_bin + rem_cap obviously allows fathoming but some algorithms will
    pack all item into the smallest remaining bin, hence min_bin + rem_cap
    allows fathoming as well ! (be careful on returned value!)
    """
    if min_bin + rem_cap <= lower_bound:
        # useless branch
        return lower_bound

    bb = [b for b in bins]
    bb.sort(key=lambda x: x.remaining, reverse=True)
    best_stretch = max(max_bin,lower_bound)
    for w in weights:
        if w > rem_cap: continue
        it = Item(w)
        if not is_feasible_instance(bb, it): continue
        if min_bin + w >= upper_bound:
            return upper_bound
        prev_rem = -1
        stretch = upper_bound
        for b in bb:
            if b.remaining == prev_rem:
                # try a single bin for any given couple (item weight, bin weight)
                continue
            prev_rem = b.remaining
            b.force_add(it)
            # upper_bound is updated to current min stretching factor for this item
            # lower bound is updated to the best stretching factor on all items.
            val = solve(memo, bb, best_stretch, stretch, rem_cap-w, weights)
            b.rem_last()
            stretch = min(val, stretch)
            if stretch <= best_stretch: break
        if stretch >= upper_bound:
            # item w gives a good enough solution
            return upper_bound
        if stretch > best_stretch:
            best_item = w
            best_stretch = stretch

    return best_stretch


################## Main routines ####################
def make_parser():
    parser = argparse.ArgumentParser(
        description='Finds the biggest lower bound achievable by\
            an adversary for the bin stretching problem in given space')
    parser.add_argument('capacity', metavar='C', type=int, nargs=1,
            help = 'bin capacity (items 1, 2,..., C are allowed)')
    parser.add_argument('nbins', metavar='N', type=int, nargs=1,
            help = 'number of bins')
    return parser

def main():
    p = make_parser()
    args = p.parse_args()
    size = args.capacity[0]
    nbins = args.nbins[0]

    print "Integer Programming solver used = "+IPSolver
    print "==========="
    print "Packing items of size 1 to %s into %s bins" % (size,nbins)

    t0 = time.time()
    res = run(range(1,size+1), num_bins=nbins, capacity=size,\
            lower_bound=4*size/3)   # We want to improve 4/3 lower bound
    t0 = time.time() - t0

    print "Stretching factor:\t\t\t%s/%s\t= %s" % (res,size,float(res)/size)

    print "Time spent verifying feasibility:\t\t  %s" % ttime
    print "Total elapsed time:\t\t\t\t  %s" % t0

if __name__ == "__main__":
    main()
