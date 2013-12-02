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

import random


################## Items management ####################

class Item:
    """ An item """
    def __init__(self, size):
        self.size = size

    def __str__(self):
        return "Size : "+str(self.size)

    def __repr__(self):
        return str(self.size)

    def __cmp__(self,other):
        return cmp(self.size,other.size)

    # For addition of two Items
    def __add__(self,other):
        return Item(self.size + other.size)

    # For sum or addition with int
    def __radd__(self,other):
        return Item(self.size + other)


################## Bins management ####################

# For efficient decreasing remaining capacity sort, use :
# y.sort(key=lambda x: x.remaining, reverse=True)

def bin_factory(num_bins, capacity=1):
    bins = []
    for i in xrange(num_bins):
        bins.append(Bin(capacity))

    return bins;

def clean_bins(bins):
    for b in bins:
        b.clean()

class Bin:
    """ A bin """
    def __init__(self, capacity=1):
        self.capacity = capacity
        self.remaining = capacity
        self.items = []

    def __str__(self):
        strn = "   Used : "+str(self.capacity-self.remaining)
        strn += "\t   Items : "+str(self.items)
        strn += "\t   (sum = "
        if sum(self.items):
            strn += str(sum(self.items).size)
        else:
            strn += "0"
        strn += ")"
        return strn

    def __repr__(self):
        #return "("+str(self.capacity-self.remaining)+", "+str(self.remaining)+")"
        return str(self.used())

    def __cmp__(self, other):
        return cmp(other.remaining, self.remaining)

    def add(self, item):
        if (not isinstance(item, Item)) or (item.size > self.remaining):
            return False
        self.remaining -= item.size
        self.items.append(item)
        return True

    def force_add(self, item):
        self.remaining -= item.size
        self.items.append(item)

    def rem_last(self):
        if not self.items:
            return False
        self.remaining += self.items.pop().size
        return True

    def used(self):
        return self.capacity-self.remaining

    def clean(self):
        self.remaining = self.capacity
        self.items = []


################## Generator ####################

def generate_instance(num_bins, capacity=1, full=False, rounding=2):
    """
    Generates a n bins instance, all full if full is True
    Returns the item list and the assignment

    Keyword arguments:
    num_bins -- number of bins
    capacity -- bin capacity (default 1.0)
    full -- if True, ensures all bins are full (default False)
    rounding -- number of digits (default 2)
    """
    bins = bin_factory(num_bins, capacity)
    items = []
    i = 0
    while (i < num_bins):
        current_bin = bins[i]
        x = random.random()
        if (rounding): x = round(x, rounding)
        item = Item(x)
        if current_bin.add(item):
            items.append(item)
            continue
        # Item cannot be added to the current bin
        if full:
            item = Item(current_bin.remaining)
            b = current_bin.add(item)
            assert(b)
            items.append(item)
        i += 1

    random.shuffle(items)
    return items, bins


def main():
    print("Instance de bin packing avec 3 bins :")
    x,y = generate_instance(3)
    print(x)
    y.sort(reverse=True)
    print(y)
    print(y[0])
    x = Item(5)
    y = Item(3.4)
    z = Item(0.1)
    h=[x,y,z]
    assert(x+y == Item(8.4))
    assert(sum(h) == Item(8.5))


if __name__ == "__main__":
    main()
