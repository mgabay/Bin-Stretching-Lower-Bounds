from bins import *


def fail(items, bins, item):
    print "Failed"
    print "Bins: "
    for b in bins:
        print b
    print "\nFailed on item with size: "+str(item.size)
    print "Remaining items: "+str(items)

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


def run(threshold):
    print ("Running with threshold = "+str(threshold))
    max_size = 1 + threshold
    i = 0
    while True:
        i += 1
        if (i % 10**4 == 0): print "Iteration "+str(i)
        n = int(round(100*random()) + 1)
        items, y = generate_instance(n,full=True)
        bins = bin_factory(n, max_size)
        if not first_fit(items, bins):
            print("Failed at iteration "+str(i))
            print("Max stretched size = "+str(max_size))
            break


def main():
    stretch_factor = 0.39
    while True:
        stretch_factor += .01
        run(stretch_factor)


if __name__ == "__main__":
    main()
