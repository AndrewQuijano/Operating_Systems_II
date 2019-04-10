#!/usr/bin/python

# --------------------------------------------------------
#   Network Packet Sniffer:
#       parses packet data, generates connection records
#
#    Authors: Daniel Mesko
# --------------------------------------------------------


import pyshark


# GLOBAL TODO:
   #  - NEED TO DERIVE Time-Based features!! So calculate 2sec from timestamp?
   #        ...or should read directly from wire in this module?
   #  - NEED TO DERIVE 100 connection window features
   # WILL NEED to sort by same dest.host, same service, and do with time windows



# An object for individual packets, with members for all relevant
#    header information
class Packet:

    # protocol-specific members set as None in constructor
    def __init__(self, con_no, protocol, service, src_ip, dst_ip, src_port, 
            dst_port, time_elapsed, size, urgent): 
        self.con_no = con_no
        self.protocol = protocol
        self.service = service
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.time_elapsed = time_elapsed
        self.size = int(size)
        self.urgent = urgent

    def to_string(self):
        out_str = ('\nconnection_number: ' + str(self.con_no) + 
            '\nprotocol: ' + self.protocol +
            '\nservice: ' + self.service + 
            '\nsource IP: ' + str(self.src_ip) +
            '\ndestination IP: ' + str(self.dst_ip) +
            '\nsource port: ' + str(self.src_port) +
            '\ndestination port: ' + str(self.dst_port) +
            '\npacket size: ' + str(self.size) +
            '\nurgent flag: ' + str(self.urgent) + 
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

    # TODO: This is just a pretty printer...remove it?
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

    def to_csv(self):
        out_str = (str(self.duration) + ',' + 
            self.protocol + ',' +
            self.service + ',' +
            str(self.flag) + ',' + 
            str(self.src_bytes) + ',' +
            str(self.dst_bytes) + ',' +
            str(self.land) + ',' +
            str(self.wrong_fragments) + ',' +
            str(self.urgent) + ',')
        return out_str


# TODO: catch attribute errors!
def collect_connections(pcap_file):

    cap = pyshark.FileCapture(pcap_file)
    raw_connections = {}
    connections = []

# ----------------------------------------------------------------
# Collect packets from the same connection, create connection dict
# ----------------------------------------------------------------
    for pkt in cap:
        if 'tcp' in pkt:
            key = "tcp_conn"+pkt.tcp.stream
            pkt_obj = Packet(pkt.tcp.stream, 'TCP', pkt.highest_layer,
                    pkt.ip.src, pkt.ip.dst,
                    pkt.tcp.srcport, pkt.tcp.dstport, pkt.tcp.time_relative,
                    pkt.length, 0)#pkt.tcp.flags.urg)
        elif 'udp' in pkt:
            # TODO: why doesn't pkt.udp.time_relative work?? didn't it used to?
            key = "udp_conn"+pkt.udp.stream
            pkt_obj = Packet(pkt.udp.stream, 'UDP', pkt.highest_layer, 
                    pkt.ip.src, pkt.ip.dst,
                    pkt.udp.srcport, pkt.udp.dstport, 0,#pkt.udp.time_relative,
                    pkt.length, 0)
        else:
            # do not record packets that aren't TCP/UDP
            continue

        if key not in raw_connections.keys():
            raw_connections[key] = [pkt_obj]
        else:
            lst = raw_connections[key]
            lst.append(pkt_obj)



# -------------------------------------------------------------------------
# Derive basic features of each connection, create Connection objects, list
# -------------------------------------------------------------------------
    for k,v in raw_connections.items():

        src_bytes = 0
        dst_bytes = 0
        wrong_frag = 0
        urgent = 0
        protocol = v[0].protocol
        service = v[0].service
        duration = float(v[-1].time_elapsed)
        duration = int(duration / 1.0)
        src_ip = v[0].src_ip
        dst_ip = v[0].dst_ip
        src_port = v[0].src_port
        dst_port = v[0].dst_port

        # land feature (loopback connection)
        if (src_ip == dst_ip) and (src_port == dst_port):
            land = 1
        else:
            land = 0

        # traverse packets (some basic features are aggregated from each packet)       
        for pkt in v: 
            if src_ip == pkt.src_ip:
                src_bytes += pkt.size
            else:
                dst_bytes += pkt.size

            if pkt.urgent == 1:
                urgent += 1

       
    # TODO: WTF is status flag (why is it always SF)? I'm gonna
        #       hardcode it, but that's soooo wrong
        # ALSO....wrong fragments bit, hardcoding as 0

        # generate Connection with basic features
        record = Connection(duration, protocol, service, v, 'SF', src_bytes,
            dst_bytes, land, 0, urgent)
        
        connections.append(record)
        
# ---------------------------------------------------------------------
# Derive traffic-based features, update each Connection object
# ---------------------------------------------------------------------
    for rec in connections:
        break


# ---------------------------------------------------------------------
# Traverse Connection list, generate CSV file
# ---------------------------------------------------------------------
    output = open('records.csv', 'w')
    for rec in connections:
        output.write(rec.to_csv())
        output.write('\n')
        output.flush()
        



# pass control to collect_connections(), take all the credit
if __name__ == '__main__':
    pcap_file = 'sniff.pcap'
    collect_connections(pcap_file)
    print('\nconnection records generated, written to records.csv\n')
