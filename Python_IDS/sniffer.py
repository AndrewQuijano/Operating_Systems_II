#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#     parses packets 
#
#    Authors: Daniel Mesko and Andrew Quijano 
# --------------------------------------------------------


import pyshark

# TODO: Have to specify interface...should we take interface as input from a driver module?
capture = pyshark.LiveCapture(interface='enp0s3')

for packet in capture.sniff_continuously(packet_count=5):

    packet.pretty_print()


