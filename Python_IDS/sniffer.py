#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#     parses packets into a struct containing all header
#       fields
#
#    Authors: Daniel Mesko and Andrew Quijano 
# --------------------------------------------------------


import pyshark

capture = pyshark.LiveCapture(interface='eth0')

for packet in capture.sniff_continuously(packet_count=10):

	print("highest layer: {}".format(packet.highest_layer))


