# -*- coding: UTF-8 -*-
from random import random, shuffle


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
        x = random()
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

    shuffle(items)
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
