#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#       collects packet records into connection records
#
#    Authors: Daniel Mesko
# --------------------------------------------------------



# TODO: Have to specify interface...should we take interface as input from a driver module?

import pyshark


# collect packets into connection records
def collect_connections(pcap_file):

    cap = pyshark.FileCapture(pcap_file)
    data = ''
    connections = {}

    for pkt in cap:
        if 'tcp' in pkt:
            key = 'tcp_connection_no: ' + pkt.tcp.stream
            data = 'dong'#str(pkt.tcp.payload)
        elif 'udp' in pkt:
            key = 'udp_connection_no: ' + pkt.udp.stream
            data = str(pkt.udp.payload)
        else:
            key = 'other_transport'

        if key not in connections.keys():
            connections[key] = data
        else:
            connections[key] += ' , ' + data

if __name__ == '__main__':
    pcap_file = 'sniff.pcap'
    collect_connections(pcap_file)
    print('connection records generated\n')
