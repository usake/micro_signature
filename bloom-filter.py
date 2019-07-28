#!/usr/local/bin/python3
import argparse
import numpy as np
from datetime import datetime

def seating_calculated (nSlots, nKeys, nSeats):
    # simplify: unbit = np.power(1 - 1/nSlots, nKeys * nSeats)
    unbit = np.exp(-nSeats * nKeys / nSlots)
    # P(N) fix-factor: 1/(k+1) when sum(P(i)), i=1,2,3,...,N
    noSeat = int(nKeys / (1.0 + nSeats) * np.power(1-unbit, nSeats))
    seated = nKeys - noSeat
    print("prob_calc: seated(%d) noSeat(%d) 0-bit(%f)" % (seated, noSeat, unbit))
    return seated

def seating_simulated (nSlots, nKeys, nSeats):
    np.random.seed(datetime.now().microsecond)
    AM = np.zeros(nSlots, dtype=np.int)
    KN = np.random.randint(0, nSlots, size=(nKeys, nSeats))
    noSeat, seated = 0, 0
    for seats in KN:
        seats_available = seats[AM[seats] == 0]
        if seats_available.size > 0:
            AM[seats_available] = 1
            seated += 1
        else:
            noSeat += 1
    unbit = 1.0 * len(AM[AM == 0]) / nSlots
    print("simulated: seated(%d) noSeat(%d) 0-bit(%f)" % (seated, noSeat, unbit))
    return seated

def main():
    parser = argparse.ArgumentParser(description='simulate and compare hash k-seating issue')
    parser.add_argument("-m", "--nSlots", type=int, help="number of Hash table slots")
    parser.add_argument("-n", "--nKeys", type=int, help="allowed max Hash keys")
    args = parser.parse_args()
    M, N = int(args.nSlots), int(args.nKeys)
    # the best k (bits) for bloom-filter is integer round(4-drop-5-add) of ln(2)*M/N
    k = int(0.5 + np.log(2) * M / N)
    print("M N k", M, N, k)
    pin = seating_calculated(M, N, k)
    sin = seating_simulated(M, N, k)
    print("pin/sin = %f" % (pin/sin))

if __name__ == '__main__':
    main()
