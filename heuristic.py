from bins import *


def first_fit(items, bins):
    """
    First fit heuristic:
        place an item in the bin with the
        smallest remaining space possible

    Bins might be empty or not
    """

    while items:
        #bins.sort(reverse=True)
        bins.sort(key=lambda x: x.remaining, reverse=False)
        i = items.pop()
        added = False
        for b in bins:
            if b.add(i):
                added = True
                break
        if not added:
            #fail(items, bins, i)
            return False

    return True
