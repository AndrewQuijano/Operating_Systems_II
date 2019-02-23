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

#TODO: Figure out interface with ML stuff...
#         Extract features, pass back as object to a separate thread for ML calcs ?
def handle_packet(pkt):
    try:
        print("highest layer" + str(pkt.highest_layer))
        protocol =  pkt.transport_layer
        src_addr = pkt.ip.src
        src_port = pkt[pkt.transport_layer].srcport
        dst_addr = pkt.ip.dst
        dst_port = pkt[pkt.transport_layer].dstport
        print ('%s  %s:%s --> %s:%s  %s ' % (protocol, src_addr, src_port, dst_addr, dst_port, pkt.de))
    except AttributeError as e:
        pass
 
capture.apply_on_packets(handle_packet, timeout=100)
