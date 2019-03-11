#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#       collects packet records into connection records
#
#    Authors: Daniel Mesko
# --------------------------------------------------------


import pyshark

class Packet:

    # protocol-specific members set as None in constructor
    def __init__(self, con_no, src_ip, dst_ip, src_port, dst_port): 
        self.con_no = con_no
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.time_elapsed = None

    def to_string(self):
        out_str = ('\ntcp_connection_number: ' + str(self.con_no) + 
            '\nsource IP: ' + str(self.src_ip) +
            '\ndestination IP: ' + str(self.dst_ip) +
            '\nsource port: ' + str(self.src_port) +
            '\ndestination port: ' + str(self.dst_port) +
            '\ntime elapsed since first packet of connection: ' + 
            str(self.time_elapsed) + 
            '\n')
        return out_str


# unnecessary?
class Connection:

    def __init__(self, duration):
        self.duration = duration



# collection function
def collect_connections(pcap_file):

    cap = pyshark.FileCapture(pcap_file)
    data = ''
    connections = {}

    # collect packets into connection records
    for pkt in cap:
        if 'tcp' in pkt:
            key = "tcp_conn"+pkt.tcp.stream
            pkt_obj = Packet(pkt.tcp.stream, pkt.ip.src, pkt.ip.dst,
                    pkt.tcp.srcport, pkt.tcp.dstport)
            pkt_obj.time_elapsed = pkt.tcp.time_relative
        elif 'udp' in pkt:
            key = "udp_conn"+pkt.udp.stream
            pkt_obj = Packet(pkt.udp.stream, pkt.ip.src, pkt.ip.dst,
                    pkt.udp.srcport, pkt.udp.dstport)
        else:
            # do not record packets that aren't TCP/UDP
            continue

        if key not in connections.keys():
            connections[key] = [pkt_obj]
        else:
            lst = connections[key]
            lst.append(pkt_obj)



    # derive features, generate output file
#    out_file = open('packets.csv', 'w')
    for k,v in connections.items():
        out_file = k + '.bin'
        output = open(out_file, 'w')
        
        for pkt in v:
            output.write(pkt.to_string())
            output.flush()




if __name__ == '__main__':
    pcap_file = 'sniff.pcap'
    collect_connections(pcap_file)
    print('\nconnection records generated\n')
