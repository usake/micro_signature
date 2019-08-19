#!/usr/bin/env python3

# https://www.cnblogs.com/liun1994/p/6142505.html -- tshark to compare result
# https://blog.csdn.net/weixin_34342992/article/details/88004374 -- pcap instruction

import pcap # pip3 install pypcap
import dpkt # pip3 install dpkt
from binascii import hexlify as he

devs = pcap.findalldevs()
print(*devs, sep=' ')
print("use [%s]" % devs[4], sep='\n')

pc = pcap.pcap(devs[4], promisc=True, immediate=True, timeout_ms=50)
pc.setfilter('tcp port 80')  

for ts, data in pc:
    print(ts, he(data))
