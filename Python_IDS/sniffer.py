#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#     parses packets into a struct containing all header
#       fields
#
#    Authors: Daniel Mesko and Andrew Quijano 
# --------------------------------------------------------


import pyshark

# TODO: Have to specify interface...should we take interface as input from a driver module?
capture = pyshark.LiveCapture(interface='en3')


for packet in capture.sniff(packet_count=10):

	print("highest layer: {}".format(packet.highest_layer))

