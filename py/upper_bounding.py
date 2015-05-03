# -*- coding: UTF-8 -*-
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
import random
import yaml
import os, sys
from tree import *
from time import gmtime, strftime

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
    # WARNING: if the order is changed then, feasibility has to be verified
    # for every item ! cf boolean feasibilityVerified in branch()

    init_solver(SOLVER, jarpath)
    if SOLVER == "CHOCO" or SOLVER == "CP":
        run_jvm(jvmpath, jarpath)

    d = {}
    if lower_bound < 0:
        lower_bound = capacity

    root=TreeNode()
    root.attr['Name']="Root"
    val = branch(ws, bins, num_bins*capacity, lower_bound, 26.*capacity/17.,
            d, backtrack=root)
    root.set_input()
    #strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f = open('backtrack.dot', 'w')
    f.write(root.dot())
    f.close()

    terminate_solver(SOLVER)

    """ Memory profiling
    from guppy import hpy
    h = hpy()
    print(h.heap())
    """

    return val


ttime = 0
fcalls = 0
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

    global fcalls
    fcalls += 1
    global ttime
    t = time.time()
    r = is_feasible(items, len(bins), bins[0].capacity, SOLVER)
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
    l.sort() # break symmetries
    # MEMORY: spare some memory by removing the following line:
    l.append(-1)
    # separate bins from items / use less memory than making a list of tuples...
    # not required here since the number of bins is fixed
    for i, j in d.items():
        l.append(i)
        l.append(j)

    return binascii.rlecode_hqx(bytes(' '.join(str(i) for i in l),'UTF-8'))
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


def store(memo, t, lower_bound, upper_bound, ret):
    if not t in memo:
        memo[t] = (lower_bound,upper_bound,ret)
        return
    # We know that lb < ub and:
    # (val >= ub and ub < upper_bound) || (val <= lb and lb > lower_bound)
    lb, ub, val = memo[t]
    if val >= ub and ub < upper_bound:
        memo[t] = (min(lower_bound,lb), upper_bound, max(ret,val))
    elif val <= lb and lb > lower_bound:
        memo[t] = (lower_bound, max(upper_bound,ub), min(ret,val))
    else:
        raise NameError("Memo issue: both tests shall not fail")


def solve(memo, bins, lower_bound, upper_bound, rem_cap, weights, backtrack):
    t = make_key(bins)
    ret = recall(memo, t, lower_bound, upper_bound)
    if ret:
        backtrack.attr['cut'] = "Memoized value"
        #backtrack.attr['val'] = ret
        return ret
    ret = branch(weights, bins, rem_cap, lower_bound, upper_bound,
            memo, backtrack)
    #store(memo, t, lower_bound, upper_bound, ret)
    memo[t] = (lower_bound,upper_bound,ret)
    return ret


####### End Memoization #######

nodes = 0
def branch(weights, bins, rem_cap, lower_bound, upper_bound, memo={},
        backtrack=False):
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
    global nodes
    nodes += 1
    if not bins:
        raise NameError('Branching to pack items in... no bins!')
    assert rem_cap >= 0
    if lower_bound >= upper_bound:
        backtrack.attr['cut'] = "LB >= UB"
        return lower_bound

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
        backtrack.attr['cut'] = "Wmax >= UB"
        return max_bin

    """
    The condition: if max_bin + rem_cap <= lower_bound: fathom
    is obvious. However, some deterministic algorithms will pack all of
    the remaining items into current smallest bin.
    Hence, min_bin + rem_cap allows fathoming as well !
    """
    if min_bin + rem_cap <= lower_bound:
        # useless branch
        backtrack.attr['cut'] = "Cannot improve"
        return lower_bound

    bb = sorted(bins, key=lambda x: x.remaining, reverse=False)
    best_stretch = max(max_bin,lower_bound)
    best_sons = []
    feasibilityVerified = False
    for w in weights:
        if w > rem_cap: continue
        it = Item(w)
        #if not is_feasible_instance(bb, it): continue
        if not feasibilityVerified:
            if not is_feasible_instance(bb, it): continue
            feasibilityVerified = True
        if min_bin + w >= upper_bound:
            backtrack.attr['cut'] = "Wmin + "+str(w)+" >= UB"
            return min_bin + w
        prev_rem = -1
        stretch = upper_bound
        sons = []
        for b in bb:
            if b.remaining == prev_rem:
                # try a single bin for any given couple (item weight, bin weight)
                continue
            prev_rem = b.remaining
            b.force_add(it)

            bt = TreeNode()
            bt.attr['bins'] = [u.used()
                    for u in sorted(bins, key=lambda x: id(x))]
            sons.append(bt)

            # upper_bound is updated to current min stretching factor for this item
            # lower bound is updated to the best stretching factor on all items.
            val = solve(memo, bb, best_stretch, stretch, rem_cap-w,
                    weights, bt)

            b.rem_last()
            stretch = min(val, stretch)
            if stretch <= best_stretch: break
        if stretch >= upper_bound:
            # item w gives a good enough solution
            backtrack.attr['Next weight'] = w
            #backtrack.attr['val'] = stretch
            backtrack.extend(sons)
            return stretch
        if stretch > best_stretch:
            backtrack.attr['Next weight'] = w
            best_stretch = stretch
            best_sons = sons

    #backtrack.attr['val'] = best_stretch
    backtrack.extend(best_sons)
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
    parser.add_argument('-r', nargs=1, type=int,
            help='Generates R random numbers in 1..C')
    return parser

def config():
    # Parse config file
    dirn = os.path.dirname(sys.argv[0])
    cnf = os.path.abspath(dirn) + '/config.conf'
    stream = open(cnf)
    conf = yaml.load(stream)
    stream.close()

    # Set config
    global SOLVER, jvmpath, jarpath
    if 'solver' in conf:
        SOLVER = conf['solver']
    else: SOLVER = 'CHOCO'
    if 'jvmpath' in conf:
        jvmpath = conf['jvmpath']
    if 'jarpath' in conf:
        jarpath = os.path.abspath(dirn) + '/' + conf['jarpath']
    else: jarpath = os.path.abspath(dirn) + '/../lib/'

def main():
    # Parse options
    p = make_parser()
    args = p.parse_args()
    size = args.capacity[0]
    nbins = args.nbins[0]
    r = args.r

    # Parse config file and set options
    config()

    print("Solver used = "+SOLVER)
    print("===========")
    print("Packing items of size 1 to %s into %s bins" % (size,nbins))

    if r:
        weights = random.sample(range(1,size+1), r[0])
    else:
        weights = range(1,size+1)
    weights = list(weights) # for python 2/3 compatibility
    weights.sort()

    print("Weights = %s" % (weights))

    lb = 4*size / 3
    t0 = time.time()
    res = run(weights, num_bins=nbins, capacity=size,\
            lower_bound=lb)   # We want to improve 4/3 lower bound
    t0 = time.time() - t0

    if res == lb:
        print("\nStretching factor <= %f" % (float(lb)/size))
    else:
        print("\nStretching factor improved:\t\t%s/%s\t= %s" % (res,size,float(res)/size))

    print("Feasibility checks:\t\t\t\t  %s" % fcalls)
    print("Time spent verifying feasibility:\t\t  %s" % ttime)
    print("#nodes:\t\t\t\t\t\t  %s" % nodes)
    print("Total elapsed time:\t\t\t\t  %s" % t0)

if __name__ == "__main__":
    main()
