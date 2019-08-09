#!/usr/bin/env python3

import pcap # pip install pypcap
import dpkt # pip install dpkt
from binascii import hexlify as he

devs = pcap.findalldevs()
print(*devs, sep=' ')
print("use [%s]" % devs[4], sep='\n')

pc = pcap.pcap(devs[4], promisc=True, immediate=True, timeout_ms=50)
pc.setfilter('tcp port 80')

for ts, data in pc:
    print(ts, he(data))
