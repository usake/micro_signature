#!/usr/bin/env python3
import argparse
import numpy as np
from datetime import datetime
from binascii import unhexlify as unhex
from pybloomfilter import BloomFilter
np.random.seed(datetime.now().microsecond)


# n - Keys, m - Slots, k - Seats

def seating_calculated (m, n, k):
    p0 = np.exp(-k*n/m) # simplify from np.power(1-1/m, n*k)
    p1 = 1 - p0
    p_add_collision = np.power(p1, k) # when n-1 item added
    # Prob(N) fix-factor: 1/(k+1) when sum(P(i)^k), i=1,2,3,...,N
    p_add_collision_mean = p_add_collision / (1 + k)
    add_no = int(n * p_add_collision_mean)
    add_ok = n - add_no
    print("prob_calc: add_ok=(%d) add_no=(%d) p(bit-0)=(%.12f)" % (add_ok, add_no, p0))
    return add_ok

def seating_simulated (data, n, k, filter_filename=None):
    print("len(data)=%d" % len(data))
    add_ok, add_no, add_re, repeats = 0, 0, 0, 0
    add_repeat_but_bf_add_true = 0
    bf = BloomFilter(n, 1/np.power(2,k), filter_filename)
    duniq = set()
    for d in data:
        if d not in duniq:
            duniq.add(d)
            repeated = False
        else:
            repeats += 1
            repeated = True
        result = bf.add(d)
        if result == False:
            add_ok += 1
            if repeated:
                add_repeat_but_bf_add_true += 1
        elif result == True:
            if repeated:
                add_re += 1
            else:
                add_no += 1
    bfcount = len(bf)
    print("simulated: add_ok=(%d) add_no=(%d) add_re=(%d) repeats=(%d)" % (add_ok, add_no, add_re, repeats))
    print("add_repeat_but_bf_add_true=(%d)" % add_repeat_but_bf_add_true)
    print("bf: num_bits=%d, capacity=%d, error_rate=%f, added=%d" % (bf.num_bits, bf.capacity, bf.error_rate, bfcount))
    return add_ok

def main():
    parser = argparse.ArgumentParser(description='simulate and compare hash k-seating issue')
    parser.add_argument("-k", "--hashes", type=int, help="number of Hash functions`")
    parser.add_argument("-n", "--capacity", type=float, help="allowed max items to add")
    args = parser.parse_args()
    # the best k (bits) for bloom-filter is integer round(4-drop-5-add) of ln(2)*M/N
    # M=10^9+7,K=8 ==> capacity=86643398.1765
    M = int(args.capacity * args.hashes / np.log(2))
    N, K = int(args.capacity), int(args.hashes)
    print("M N K M/N: ", M, N, K, M/N)
    pin = seating_calculated(M, N, K)
    data = list([np.random.bytes(5) for i in range(N)])
    sin = seating_simulated(data, N, K, 'myfiltername')
    print("pin/sin = %f" % (pin/sin))

if __name__ == '__main__':
    main()
