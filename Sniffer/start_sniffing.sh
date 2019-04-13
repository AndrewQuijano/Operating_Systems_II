#!/bin/bash


# TODO: Take number of packets/timeout as arg?
#         take interface name as arg?

echo "reading raw packet data from the wire"
sudo tcpdump -c 200 -s0 -i enp0s3 -w sniff.pcap
python3 collect.py
#echo "feeding connection records into ML module"


# clean up
sudo rm sniff.pcap
#sudo rm packets.csv

