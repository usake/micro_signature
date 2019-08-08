#!/bin/bash

pcapfile=$1
streams=/tmp/stream_ids
N=$(tshark -r $pcapfile -T fields -e tcp.stream | sort -n | uniq | tee $streams | wc -l)
cat $streams | \
while read stream; do
  echo -n "saving stream $stream ..."
  tshark -r $pcapfile -F pcap -w stream-${stream}.pcap -2 -R "tcp.stream==${stream}" && echo "done" || echo "fail"
done | \
tqdm --unit stream --unit_scale --total $N
