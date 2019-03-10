#!/bin/bash

# take number of packets to sniff as arg?

sudo tcpdump -c 20 -s0 -i enp0s3 -w sniff.pcap
python3 collect.py

# tshark -r sniff.pcap -T fields -e frame.time -e ip.flags -e ip.src -e ip.dst -e ip.proto -e tcp.connection.fin -e tcp.dstport -e tcp.srcport -E header=y -E separator=, -E quote=d -E occurrence=f > packets.csv


# clean up
sudo rm sniff.pcap


