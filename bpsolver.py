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
Solver to the bin packing problem, using integer programming
"""

#import sys
#sys.path.extend(['', '/usr/local/lib/python2.7/dist-packages/PuLP-1.5.4-py2.7.egg', '/usr/local/lib/python2.7/dist-packages/pyparsing-1.5.7-py2.7.egg', '/usr/local/lib/python2.7/dist-packages/py4j-0.8-py2.7.egg', '/home/scrat/Dropbox/PhD/bin stretching/ub', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-linux2', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages','/usr/lib/python2.7/dist-packages/PIL', '/usr/lib/python2.7/dist-packages/gst-0.10', '/usr/lib/python2.7/dist-packages/gtk-2.0', '/usr/lib/pymodules/python2.7', '/usr/lib/python2.7/dist-packages/ubuntu-sso-client', '/usr/lib/python2.7/dist-packages/ubuntuone-client', '/usr/lib/python2.7/dist-packages/ubuntuone-control-panel', '/usr/lib/python2.7/dist-packages/ubuntuone-couch', '/usr/lib/python2.7/dist-packages/ubuntuone-storage-protocol'])

from pulp import *
#import yaposib
#from gurobipy import *

import jpype
from py4j.java_gateway import JavaGateway, GatewayClient

import os
import random
import binascii

from bins import *
from heuristic import *


################## Bin Packing modeling ####################

# Memorize problem solved
mem = {}

def make_key(items, num_bins, capacity):
    d = {}
    for i in items:
        s = i.size
        if s in d: d[s] += 1
        else: d[s] = 1
    l = []
    for i, j in d.iteritems():
        l.append(i)
        l.append(j)

    # MEMORY: if num_bins and capacity never change, spare some memory
    # by removing the following 2 lines:
    l.append(num_bins)
    l.append(capacity)

    return binascii.rlecode_hqx(' '.join(str(i) for i in l))
    #return tuple(l)

calls = 0
def is_feasible(items, num_bins, capacity, solver="GLPK"):
    ret, res = is_trivial(items, num_bins, capacity)
    if ret:
        return res
    global mem
    t = make_key(items, num_bins, capacity)
    if t in mem:
        return mem[t]
    ret, res = heuristics(items, num_bins, capacity)
    if ret:
        sol = res
        mem[t] = sol
        return sol

    """
    Current implemented bound is not interesting enough
    m = compute_min_bins(items, capacity)
    if m > num_bins:
        sol = False
        mem[t] = sol
        return sol
    else:
    """

    global calls
    calls += 1
    sys.stdout.write("\rCP calls:\t%d" %calls)
    sys.stdout.flush()

    if solver == "CHOCO" or solver == "CP":
        sol = CPSolve(items, num_bins, capacity)

    if solver == "CHOCO4J" or solver == "CP4J":
        sol = py4j_solve(items, num_bins, capacity)

    else:
        mod = make_model(items, num_bins, capacity)
        sol = solve(mod, solver)
    #sol = grb_solve(items, num_bins, capacity)
    #assert grb_solve(items, num_bins, capacity) == sol

    mem[t] = sol
    return sol

def make_model(items, num_bins, capacity):
    ritems = xrange(len(items))
    rbins = xrange(num_bins)
    prob = LpProblem("Bin Packing Feasibility",LpMinimize)
    prob += 0, "No objective: feasibility problem"
    var = {(i,j): LpVariable("x("+str(i)+","+str(j)+")",0,1,LpBinary)\
            for i in ritems for j in rbins}

    # Big item assignments can be fixed from the beginning
    items.sort(reverse=True)
    cur = 0
    count = 0
    half = 0
    for i in items:
        if 2*i.size < capacity:
            break
        prob += var[(count,cur)] == 1,\
                "Fixing item "+str(count)+" to bin "+str(cur)
        if 2*i.size == capacity and half == 0:
            half = 1
        else:
            half = 0
            cur += 1
        count += 1

    # If there were no big item, we can still fix the first one
    if count == 0:
        prob += var[(0,0)] == 1, "First item symmetry breaking"

    for i in ritems:
        prob += lpSum(var[(i,j)] for j in rbins) == 1,\
                "Assign item "+str(i)

    """
    # Symmetry breaking constraints of assignement
    prev = -1
    for i in ritems:
        if items[i].size != prev:
            prev = items[i].size
            continue
        for j in rbins:
            prob += lpSum(var[(i-1,k)] for k in xrange(j+1)) >= var[(i,j)],\
                "Breaking symmetry, "+str((i,j))
    """

    for j in rbins:
        prob +=\
            lpSum(var[(i, j)]*items[i].size for i in ritems) <= capacity,\
            "Capacity constraint for bin "+str(j)

    return prob


def is_trivial(items, num_bins, capacity):
    # Assumes that all items are smaller than the capacity
    """
    for i in items:
        if i.size > capacity:
            return True, False
    """

    if len(items) <= num_bins:
        return True, True

    # compute sum of items and try first-fit
    sm = 0
    cur = capacity
    idx = 0
    for i in items:
        s = i.size
        sm += s
        if cur >= s: cur -= s
        else:
            cur = capacity - s
            idx += 1

    if idx < num_bins:
        return True, True
    if sm > num_bins*capacity:
        return True, False

    return False, True

def heuristics(items, num_bins, capacity):
    # First-Fit Increasing
    items.sort(reverse=True)
    if (len(items) <= num_bins): # defensive: verified in is_trivial
        return True, True
    if (items[num_bins-1].size + items[num_bins].size > capacity):
        return True, False
    big = 0
    half = 0
    idx = 0
    cur = capacity
    for i in items:
        s = i.size
        if 2*s > capacity: big += 1
        elif 2*s == capacity: half += 1
        if cur >= s: cur -= s
        else:
            cur = capacity - s
            idx += 1

    if idx < num_bins:
        return True, True
    if 2*big + half > 2*num_bins:
        return True, False

    # BFD
    #items.sort(reverse=True)
    tmp_bins = bin_factory(num_bins, capacity)
    if first_fit(items, tmp_bins):
        return True, True

    # Randomized best fit
    #for i in xrange(max(2,capacity-8)):
    #    clean_bins(tmp_bins)
    #    random.shuffle(items)
    #    if first_fit(items, tmp_bins):
    #        return True, True

    return False, True


def solve(model, solver="GLPK"):
    if solver == "CPLEX":
        model.solve(CPLEX(msg=0))
    elif solver == "GUROBI":
        model.solve(GUROBI(msg=0))
    elif solver == "COIN":
        model.solve(COIN(msg=0))
    elif solver == "CBC":
        model.solve(PULP_CBC_CMD(msg=0))
    else:
        #model.solve(YAPOSIB(msg=0,warning=0))
        model.solve(GLPK(msg=0))

    if model.status == 1:
        return True

    return False


def grb_solve(items, num_bins, capacity):
    ritems = xrange(len(items))
    rbins = xrange(num_bins)

    # Model
    m = Model("Bin Packing Feasibility")

    # dvar item is in/out
    var = {(i,j): m.addVar(name="x(%s,%s)" % (i,j),vtype=GRB.BINARY)\
            for i in ritems for j in rbins}

    # Update model to integrate new variables
    m.update()

    # Objective
    #m.setObjective(0)

    # Big item assignments can be fixed from the beginning
    items.sort(reverse=True)
    cur = 0
    count = 0
    half = 0
    for i in items:
        if 2*i.size < capacity:
            break
        m.addConstr(var[(count,cur)] == 1,\
                "Fixing item "+str(count)+" to bin "+str(cur))
        if 2*i.size == capacity and half == 0:
            half = 1
        else:
            half = 0
            cur += 1
        count += 1

    # If there were no big item, we can still fix the first one
    if count == 0:
        m.addConstr(var[(0,0)] == 1, "First item symmetry breaking")

    # Capacity constraint
    for i in ritems:
        m.addConstr(quicksum(var[(i,j)] for j in rbins) == 1,\
                "Assign item %s" % i)

    for j in rbins:
        m.addConstr(
            quicksum(var[(i, j)]*items[i].size for i in ritems) <= capacity,\
            "Capacity constraint for bin %s" %j)

    # Solve
    m.setParam('OutputFlag', 0)

    m.optimize()

    return m.status == GRB.status.OPTIMAL


def CPSolve(items, num_bins, capacity):
    ClassSolver = jpype.JClass("solver.BPSolver")

    items = [i.size for i in items]
    bp = ClassSolver(items, num_bins, capacity)

    return bp.isFeasible()


def run_jvm():
    jvmpath = '/usr/lib/jvm/java-6-openjdk-amd64/jre/lib/amd64/server/libjvm.so'

    jarpath = 'lib/'
    classpath = ''
    for files in os.listdir(jarpath):
        if files.endswith(".jar"):
            classpath += ':'+jarpath+files
    classpath = classpath[1:]
    cpath = '-Djava.class.path=%s' % classpath

    jpype.startJVM(jvmpath, cpath)

# Unnecessary
def close_jvm():
    jpype.shutdownJVM()


gateway = None
def py4j_run():
    global gateway
    gateway = JavaGateway()

def py4j_solve(items, num_bins, capacity):
    global gateway
    if not gateway: py4j_run()

    int_class = gateway.jvm.int
    jitems = gateway.new_array(int_class,len(items))
    for i, it in enumerate(items):
        jitems[i] = it.size

    solver = stack = gateway.entry_point.getSolver()
    solver.reset(jitems, num_bins, capacity)

    return solver.isFeasible()


################## Example ####################

def main():
    it = [Item(i+1) for i in xrange(4)]
    m = make_model(it, 2, 4)
    assert not solve(m)
    #assert not solve(m, "COIN")
    #assert not solve(m, "GUROBI")
    #assert not solve(m, "CPLEX")
    m = make_model(it, 2, 5)
    assert solve(m)
    #assert solve(m, "COIN")
    #assert solve(m, "GUROBI")
    #assert solve(m, "CPLEX")
    m = make_model(it, 3, 4)
    assert solve(m)
    #assert solve(m, "COIN")
    #assert solve(m, "GUROBI")
    #assert solve(m, "CPLEX")
    print "Dummy tests passed"

if __name__ == "__main__":
    main()
