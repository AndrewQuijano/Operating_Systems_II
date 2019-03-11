#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#       collects packet records into connection records
#
#    Authors: Daniel Mesko
# --------------------------------------------------------


import pyshark


# An object for individual packets, with members for all relevant
#    header information
class Packet:

    # protocol-specific members set as None in constructor
    def __init__(self, con_no, protocol, service, src_ip, dst_ip, src_port, 
            dst_port, time_elapsed, size): 
        self.con_no = con_no
        self.protocol = protocol
        self.service = service
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.time_elapsed = time_elapsed
        self.size = int(size)

    def to_string(self):
        out_str = ('\nconnection_number: ' + str(self.con_no) + 
            '\nprotocol: ' + self.protocol +
            '\nservice: ' + self.service + 
            '\nsource IP: ' + str(self.src_ip) +
            '\ndestination IP: ' + str(self.dst_ip) +
            '\nsource port: ' + str(self.src_port) +
            '\ndestination port: ' + str(self.dst_port) +
            '\npacket size: ' + str(self.size) + 
            '\ntime elapsed since first packet of connection: ' + 
            str(self.time_elapsed) + 
            '\n')
        return out_str


# An object for representing a single connection, with connection-based
#   features as members
class Connection:

    def __init__(self, duration, protocol, service, packets, flag,
            src_bytes, dst_bytes, land, wrong_fragments, urgent):
        self.duration = duration
        self.protocol = protocol
        self.service = service
        self.packets = packets
        self.flag = flag
        self.src_bytes = src_bytes
        self.dst_bytes = dst_bytes
        self.land = land
        self.wrong_fragments = wrong_fragments
        self.urgent = urgent

    # TODO: Add connection number?
    def to_string(self):
        out_str = ('\nduration: ' + str(self.duration) +
            '\nprotocol: ' + self.protocol +
            '\nservice: ' + self.service + 
            '\nflag: ' + str(self.flag) + 
            '\nsrc_bytes: ' + str(self.src_bytes) + 
            '\ndst_bytes: ' + str(self.dst_bytes) +
            '\nland: ' + str(self.land) + 
            '\nwrong fragments: ' + str(self.wrong_fragments) +
            '\nurgent packets: ' + str(self.urgent) +
            '\nPACKETS:\n' ) #+ str(map(lambda x : x.to_string(), self.packets)) )
        return out_str


# collection function

# TODO: catch attribute errors!
def collect_connections(pcap_file):

    cap = pyshark.FileCapture(pcap_file)
    data = ''
    connections = {}

    # collect packets into connection records
    for pkt in cap:
        if 'tcp' in pkt:
            key = "tcp_conn"+pkt.tcp.stream
            pkt_obj = Packet(pkt.tcp.stream, 'TCP', pkt.highest_layer,
                    pkt.ip.src, pkt.ip.dst,
                    pkt.tcp.srcport, pkt.tcp.dstport, pkt.tcp.time_relative,
                    pkt.length)
        elif 'udp' in pkt:
            # TODO: why doesn't pkt.udp.time_relative work?? didn't it used to?
            key = "udp_conn"+pkt.udp.stream
            pkt_obj = Packet(pkt.udp.stream, 'UDP', pkt.highest_layer, 
                    pkt.ip.src, pkt.ip.dst,
                    pkt.udp.srcport, pkt.udp.dstport, 0,#pkt.udp.time_relative,
                    pkt.length)
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

        src_bytes = 0
        dst_bytes = 0
        wrong_frag = 0
        urgent = 0
        protocol = v[0].protocol
        service = v[0].service
        duration = v[-1].time_elapsed
        src_ip = v[0].src_ip
        dst_ip = v[0].dst_ip
        
        for pkt in v: 
            if src_ip == pkt.src_ip:
                src_bytes += pkt.size
            else:
                dst_bytes += pkt.size

            output.write(pkt.to_string())
            output.flush()

        record = Connection(duration, protocol, service, v, None, src_bytes,
                dst_bytes, None, None, None)

        output.write(record.to_string())
        output.flush()
        



if __name__ == '__main__':
    pcap_file = 'sniff.pcap'
    collect_connections(pcap_file)
    print('\nconnection records generated\n')
