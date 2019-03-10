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
            key = "tcp_conn"+pkt.tcp.stream
            data = str(pkt.tcp)
        elif 'udp' in pkt:
            key = "udp_conn"+pkt.udp.stream
            data = str(pkt.udp)
        else:
            key = "other_transport"

        if key not in connections.keys():
            connections[key] = data
        else:
            connections[key] += "\n" + data

    for k,v in connections.items():
        out_file = k + '.bin'
        output = open(out_file, 'w')
        output.write(v)
        output.flush()

if __name__ == '__main__':
    pcap_file = 'sniff.pcap'
    collect_connections(pcap_file)
    print('connection records generated\n')
