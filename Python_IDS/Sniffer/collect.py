#!/usr/bin/python

# --------------------------------------------------------------
#   Network Packet Sniffer:
#       a packet preprocessor that reads raw PCAP packet data,
#           aggregates packets into connection records, and 
#           extracts/derives various features of the connections
#           consistent with those of the KDD CUP 99 dataset.
#
#    Authors: Daniel Mesko
# --------------------------------------------------------------


import pyshark


# GLOBAL TODO:
   #  - NEED TO DERIVE 100 connection window features
   #  - Remove to_string pretty printers for packet/connection?
   #  - Catch Attribute Errors in packet extraction
   #  - SERIOUSLY...print all connection data just to verify features

# An object for individual packets, with members for all relevant
#    header information
class Packet:

    def __init__(self, con_no, protocol, service, src_ip, dst_ip, src_port, 
            dst_port, time_elapsed, size, timestamp, urgent): 
        self.con_no = con_no
        self.protocol = protocol
        self.service = service
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.time_elapsed = time_elapsed
        self.size = int(size)
        self.timestamp = timestamp
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
            '\nabsolute time: ' + str(self.timestamp) + 
            '\n')
        return out_str


# An object for representing a single connection, with connection-based
#   features as members
class Connection:

    # fields set to "None" in construction are filled in by other functions
    def __init__(self, src_ip, src_port, dst_ip, dst_port, timestamp, 
            duration, protocol, service, packets, flag,
            src_bytes, dst_bytes, land, wrong_fragments, urgent):
        

        # intermediate features - used for further feature derivation
        self.src_ip = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.timestamp = timestamp

        # basic features of individual connections
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
        
        # same-host, 2 sec window traffic features
        self.count = None
        self.serror_rate = None
        self.rerror_rate = None
        self.same_srv_rate = None
        self.diff_srv_rate = None

        # same-service, 2 sec window traffic features
        self.srv_count = None
        self.srv_serror_rate = None
        self.srv_rerror_rate = None
        self.srv_diff_host_rate = None

        # host-based (connection-based) traffic features, 
        #   computed over 100 connections
        self.dst_host_count = None
        self.dst_host_srv_count = None
        self.dst_host_same_srv_rate = None
        self.dst_host_diff_srv_rate = None
        self.dst_host_same_src_port_rate = None
        self.dst_host_srv_diff_host_rate = None
        self.dst_host_serror_rate = None
        self.dst_host_srv_serror_rate = None
        self.dst_host_rerror_rate = None
        self.dst_host_srv_rerror_rate = None

        
    def add_samehost_timebased_features(self, count, serror_rate, rerror_rate,
            same_srv_rate, diff_srv_rate):
        self.count = count
        self.serror_rate = serror_rate
        self.rerror_rate = rerror_rate
        self.same_srv_rate = same_srv_rate
        self.diff_srv_rate = diff_srv_rate

    def add_sameservice_timebased_features(self, srv_count, srv_serror_rate,
            srv_rerror_rate, srv_diff_host_rate):
        self.srv_count = srv_count
        self.srv_serror_rate = srv_serror_rate
        self.srv_rerror_rate = srv_rerror_rate
        self.srv_diff_host_rate = srv_diff_host_rate

    def add_hostbased_features(self, dst_host_count):
        self.dst_host_count = dst_host_count


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
            '\n')
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
            str(self.urgent) + ','
            'THIS IS WHERE CONTENT-FEATURES GO,' +
            str(self.count) + ',' +
            str(self.srv_count) + ',' +
            str(self.serror_rate) + ',' +
            str(self.srv_serror_rate) + ',' +
            str(self.rerror_rate) + ',' +
            str(self.srv_rerror_rate) + ',' +
            str(self.same_srv_rate) + ',' +
            str(self.diff_srv_rate) + ',' +
            str(self.srv_diff_host_rate) + ',')
        return out_str


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
                    pkt.length, pkt.sniff_timestamp, 0) #pkt.tcp.flags.urg)
        elif 'udp' in pkt:
            # TODO: why doesn't pkt.udp.time_relative work?? didn't it used to?
            key = "udp_conn"+pkt.udp.stream
            pkt_obj = Packet(pkt.udp.stream, 'UDP', pkt.highest_layer, 
                    pkt.ip.src, pkt.ip.dst,
                    pkt.udp.srcport, pkt.udp.dstport, 0,#pkt.udp.time_relative,
                    pkt.length, pkt.sniff_timestamp, 0)
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
        timestamp = v[-1].timestamp


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
           
       
    # TODO: how to catch status flag (last flag bit set)? I'm gonna
        #       hardcode it now as SF, but that's soooo wrong
        # ALSO....wrong fragments bit, hardcoding as 0

        # generate Connection with basic features
        record = Connection(src_ip, src_port, dst_ip, dst_port, timestamp, 
                duration, protocol, service, v, 'SF', src_bytes,
                dst_bytes, land, 0, urgent)
        
        connections.append(record)
        
# ---------------------------------------------------------------------
# Derive time-based traffic features (over 2 sec window)
# ---------------------------------------------------------------------
    
    # same-host/same-service feature derivation 

    #TODO: probably horribly inefficient (n^8 worst case)...what do?
    for rec in connections:
        
        samehost_connections = []
        twosec_samehost_connections = []
        twosec_samesrv_connections = []

        # traverse all connections to find samehost, sameservice
        for cmprec in connections:
            time_delta = float(rec.timestamp) - float(cmprec.timestamp)
            if (rec.dst_ip == cmprec.dst_ip):
                samehost_connections.append(cmprec)
                if (time_delta <= 2.0) and (time_delta >= 0.0):
                    twosec_samehost_connections.append(cmprec)
                    
            if (rec.service == cmprec.service):
                if (time_delta <= 2.0) and (time_delta >= 0.0):
                    twosec_samesrv_connections.append(cmprec)
            else:
                continue

        # process twosec samehost connections
        count = len(twosec_samehost_connections)
        same_srv_count = 0
        diff_srv_count = 0
        serror_count = 0
        rerror_count = 0

        for cmprec in twosec_samehost_connections:
            if (rec.service == cmprec.service):
                same_srv_count = same_srv_count + 1
            else:
                diff_srv_count = diff_srv_count + 1
            
            # TODO: do syn errors, rej errors
        
        same_srv_rate = round(same_srv_count / count, 2)
        diff_srv_rate = round(diff_srv_count / count, 2)
        rec.add_samehost_timebased_features(count, None, None,
                same_srv_rate, diff_srv_rate)

        # process twosec sameservice connections
        srv_countcount = len(twosec_samesrv_connections)
        srv_serror_count = 0
        srv_rerror_count = 0
        srv_diff_host_count = 0

        for cmprec in twosec_samesrv_connections:
            if (rec.dst_ip != cmprec.dst_ip):
                srv_diff_host_counts = srv_diff_host_counts + 1
            else:
                continue
            
            # TODO: do syn errors, rej errors

        srv_diff_host_rate = round(srv_diff_host_count / count, 2)
        rec.add_sameservice_timebased_features(count, None, None,
                srv_diff_host_rate)

# ---------------------------------------------------------------------
# Derive host-based traffic features (same host over 100 connections)
#  ---------------------------------------------------------------------

        for cmprec in samehost_connections:
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
