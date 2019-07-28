#!/usr/local/bin/python3
import argparse
import numpy as np
from datetime import datetime

def seating_calculated (nSlots, nKeys, nSeats):
    M, N, k = float(nSlots), float(nKeys), float(nSeats)
    # simpify from: noseat = ((N-1)/(k+1) + 0.5) * np.power((N-1)/M, k)
    noSeat = N / (k+1) * np.power(N/M, k)
    seated = N - noSeat
    print("prob_calc: seated(%d) noSeat(%d) load-factor(%f)" % (seated, noSeat, seated/M))
    return seated

def seating_simulated (nSlots, nKeys, nSeats):
    np.random.seed(datetime.now().microsecond)
    AM = np.zeros(nSlots, dtype=np.int)
    KN = np.random.randint(0, nSlots, size=(nKeys, nSeats))
    noSeat = 0
    for seats in KN:
        seats_available = seats[AM[seats] == 0]
        if seats_available.size > 0:
             AM[seats_available[0]] = 1
             #AM[np.random.choice(seats_available)] = 1
        else:
            noSeat += 1
    seated = len(AM[AM == 1])
    print("simulated: seated(%d) noSeat(%d) load-factor(%f)" % (seated, noSeat, 1.0*seated/nSlots))
    return seated

def main():
    parser = argparse.ArgumentParser(description='simulate and compare hash k-seating issue')
    parser.add_argument("-m", "--nSlots", type=int, help="number of Hash table slots")
    parser.add_argument("-n", "--nKeys", type=int, help="allowed max Hash keys")
    parser.add_argument("-k", "--nSeats", type=int, help="allowed max Hash re-seating")
    args = parser.parse_args()
    M, N, k = int(args.nSlots), int(args.nKeys), int(args.nSeats)
    print("M N k", M, N, k)
    pin = seating_calculated(M, N, k)
    sin = seating_simulated(M, N, k)
    print("pin/sin = %f" % (pin*1.0/sin))

if __name__ == '__main__':
    main()
