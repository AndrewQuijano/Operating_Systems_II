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
from sys import argv
from os import path
import subprocess

# GLOBAL TODO:
# - NEED TO DERIVE 100 connection window features
# - Remove to_string pretty printers for packet/connection?
# - Catch Attribute Errors in packet extraction
# - Add ICMP packet capture


# An object for individual packets, with members for all relevant
# header information


class Packet:

    def __init__(self, con_no, protocol, service, src_ip, dst_ip, src_port, 
            dst_port, flags, time_elapsed, size, timestamp, urgent): 
        self.con_no = con_no
        self.protocol = protocol
        self.service = service
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.flags = flags
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
            '\nflags: ' + self.flags +  
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
            '\nflag: ' + self.flag + 
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
            str(self.urgent) + ',' +
#'THIS IS WHERE CONTENT-FEATURES GO,' +
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


def collect_connections(pcap):

    cap = pyshark.FileCapture(pcap)
    raw_connections = {}

# ----------------------------------------------------------------
# Collect packets from the same connection, create connection dict
# ----------------------------------------------------------------
    udp_count = 0
    icmp_count = 0
    for pkt in cap:
        try:
            if 'tcp' in pkt:
                key = "tcp_conn" + pkt.tcp.stream
                raw_flags = int(str(pkt.tcp.flags), 16)

                fin_flag = ( raw_flags & 0x01 ) != 0
                syn_flag = ( raw_flags & 0x02 ) != 0
                rst_flag = ( raw_flags & 0x04 ) != 0
                psh_flag = ( raw_flags & 0x08 ) != 0
                ack_flag = ( raw_flags & 0x10 ) != 0
                urg_flag = ( raw_flags & 0x20 ) != 0
                ece_flag = ( raw_flags & 0x40 ) != 0
                cwr_flag = ( raw_flags & 0x80 ) != 0
                flags = (
                ( "CWR " if cwr_flag else "" ) +
                ( "ECE " if ece_flag else "" ) +
                ( "URG " if urg_flag else "" ) +
                ( "ACK " if ack_flag else "" ) +
                ( "PSH " if psh_flag else "" ) +
                ( "RST " if rst_flag else "" ) +
                ( "SYN " if syn_flag else "" ) +
                ( "FIN " if fin_flag else "" ) )

                urgent = 0
                if 'URG' in flags:
                    urgent = 1
            
                pkt_obj = Packet(pkt.tcp.stream, 'TCP', pkt.highest_layer,
                    pkt.ip.src, pkt.ip.dst, pkt.tcp.srcport, pkt.tcp.dstport,
                    flags, pkt.tcp.time_relative,
                    pkt.length, pkt.sniff_timestamp, urgent)

                # Test for fun to derive host data?
                #print(pkt.tcp.data)

            elif 'udp' in pkt:
                key = "udp_conn" + str(udp_count)
                udp_count = udp_count + 1
                pkt_obj = Packet(pkt.udp.stream, 'UDP', pkt.highest_layer,
                    pkt.ip.src, pkt.ip.dst,
                    pkt.udp.srcport, pkt.udp.dstport, 0, 0,
                    pkt.length, pkt.sniff_timestamp, 0)

            elif 'icmp' in pkt:
                key = "icmp_conn" + str(icmp_count)
                icmp_count = icmp_count + 1
                pkt_obj = Packet(pkt.icmp.stream, 'ICMP', pkt.highest_layer,
                                pkt.ip.src, pkt.ip.dst,
                                pkt.icmp.srcport, pkt.icmp.dstport, 0, 0,
                                pkt.length, pkt.sniff_timestamp, 0)
            else:
                continue

            # Add the Packet to Connection Record
            if key not in raw_connections.keys():
                raw_connections[key] = [pkt_obj]
            else:
                lst = raw_connections[key]
                lst.append(pkt_obj)
        except AttributeError as e:
            print(e)

# -------------------------------------------------------------------------
# Derive basic features of each connection, create Connection objects, list
# -------------------------------------------------------------------------
    connections = generate_connection_records(raw_connections)

# ---------------------------------------------------------------------
# Derive time-based traffic features (over 2 sec window)
# ---------------------------------------------------------------------

    # same-host/same-service feature derivation 
    generate_time_data(connections)

# ---------------------------------------------------------------------
# Traverse Connection list, generate CSV file
# ---------------------------------------------------------------------
    with open('records.csv', 'w') as output:
        for rec in connections:
            output.write(rec.to_csv())
            output.write('\n')
            output.flush()
    # Delete all .log files used intermediate
    subprocess.run(["rm", "-rf", "*.log"])


def generate_packet_data():
    return True


def generate_connection_records(raw_connections):
    connections = []
    for k, v in raw_connections.items():
        # TODO: does taking service layer of first packet always represent
        # the connection accurately? I think not...
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

        # connection status logging variables
        orig_syn = False
        resp_syn = False
        unwanted_synack = False
        orig_fin = False
        resp_fin = False
        orig_rst = False
        resp_rst = False
        orig_synrst = False
        resp_synackrst = False
        orig_synfin = False
        resp_synackfin = False

        # land feature (loopback connection)
        if (src_ip == dst_ip) and (src_port == dst_port):
            land = 1
        else:
            land = 0

        # traverse packets, aggregate urgent packet count, byte counts,
        # and higher-level connection/termination status (as described
        # by Wenke "Data Mining Approachces for Intrusion Detection ",
        # status codes described by https://github.com/hrbrmstr/hrbrmisc/blob/master/R/cyber-bro.r"
        i = 0
        for pkt in v:
            if src_ip == pkt.src_ip:
                src_bytes += pkt.size
            else:
                dst_bytes += pkt.size

            if pkt.urgent == 1:
                urgent += 1

            # log changes to connection status by reading packet flags
            if pkt.protocol == 'TCP':
                if src_ip == pkt.src_ip:
                    if 'SYN' in pkt.flags:
                        orig_syn = True
                    if 'FIN' in pkt.flags:
                        orig_fin = True
                        if i > 0 and ('SYN' in v[i - 1].flags):
                            orig_synfin = True
                    if 'RST' in pkt.flags:
                        orig_rst = True
                        if i > 0 and ('SYN' in v[i - 1].flags):
                            orig_synrst = True
                else:
                    if 'SYN' in pkt.flags:
                        resp_syn = True
                    if 'FIN' in pkt.flags:
                        resp_syn = True
                        if i > 0 and ('SYN ACK' in v[i - 1].flags):
                            resp_synackfin = True
                    if 'RST' in pkt.flags:
                        resp_rst = True
                        if i > 0 and ('SYN ACK' in v[i - 1].flags):
                            resp_synackrst = True
            i = i + 1

        # TODO: Rethink the order of these/ if-elif structure, lots of things fall through
        # Now that connection status is aggregated from packet flags,
        # determine the status flag to set
        if protocol == 'UDP':
            status_flag = 'SF'
        elif protocol == 'TCP':
            if orig_syn and (not resp_syn) or (resp_syn and (not orig_syn)):
                status_flag = 'S0'
            elif orig_syn and resp_syn and (not orig_fin and not resp_fin):
                status_flag = 'S1'
            elif orig_syn and resp_syn and orig_fin and resp_fin and src_bytes == 0:
                status_flag = 'REJ'  # TODO: Is this really how you detect a rejected connection?
            elif orig_syn and resp_syn and orig_fin and resp_fin:
                status_flag = 'SF'
            elif orig_syn and resp_syn and (orig_fin and not resp_fin):
                status_flag = 'S2'
            elif orig_syn and resp_syn and (resp_fin and not orig_fin):
                status_flag = 'S3'
            elif orig_synrst and (not resp_syn):
                status_flag = 'RSTOS0'
            elif resp_synackrst and (not orig_syn):
                status_flag = 'RSTRH'
            elif orig_syn and resp_syn and orig_rst:
                status_flag = 'RSTO'
            elif resp_rst:
                status_flag = 'RSTR'
            elif orig_syn and orig_fin and (not resp_syn):
                status_flag = 'SH'
            elif resp_syn and resp_fin and (not orig_syn):
                status_flag = 'SHR'
            elif not orig_syn and not resp_syn:
                status_flag = 'OTH'
            else:
                status_flag = 'OHMYGOD'  # TODO: is this a bad default value? why do things fall through?
        # Maybe all flags above are TCP ONLY?
        else:
            # TODO: are there flags for ICMP?
            print("ICMP")


        # TODO: wrong fragments bit, hard-coding as 0

        # generate Connection with basic features
        record = Connection(src_ip, src_port, dst_ip, dst_port, timestamp,
                            duration, protocol, service, v, status_flag, src_bytes,
                            dst_bytes, land, 0, urgent)
        connections.append(record)

#        dummy_fn = str(k) + ".log"
#        with open(dummy_fn, "w") as dummy:
#            dummy.write(record.to_string())
#           dummy.flush()

    return connections


def generate_time_data(connections, seconds=2.0):
    # TODO: probably horribly inefficient (n^8 worst case)...what do?
    #           change counters during first passthrough?
    for rec in connections:
        samehost_connections = []
        twosec_samehost_connections = []
        twosec_samesrv_connections = []

        # traverse all connections to find samehost, sameservice
        for cmprec in connections:
            time_delta = float(rec.timestamp) - float(cmprec.timestamp)
            if rec.dst_ip == cmprec.dst_ip:
                samehost_connections.append(cmprec)
                if (time_delta <= seconds) and (time_delta >= 0.0):
                    twosec_samehost_connections.append(cmprec)

            if rec.service == cmprec.service:
                if (time_delta <= seconds) and (time_delta >= 0.0):
                    twosec_samesrv_connections.append(cmprec)
            else:
                continue

        # process two second same host connections
        count = len(twosec_samehost_connections)
        same_srv_count = 0
        diff_srv_count = 0
        serror_count = 0
        rerror_count = 0

        for cmprec in twosec_samehost_connections:
            if rec.service == cmprec.service:
                same_srv_count = same_srv_count + 1
            else:
                diff_srv_count = diff_srv_count + 1

            # TODO: Is this how you identify SYN errors?
            if cmprec.flag == 'S0':
                serror_count = serror_count + 1
            elif cmprec.flag == 'REJ':
                rerror_count = rerror_count + 1

        serror_rate = round(serror_count / count, 2)
        rerror_rate = round(rerror_count / count, 2)
        same_srv_rate = round(same_srv_count / count, 2)
        diff_srv_rate = round(diff_srv_count / count, 2)

        rec.add_samehost_timebased_features(count, serror_rate, rerror_rate,
                                            same_srv_rate, diff_srv_rate)

        # process two second same service connections
        srv_count = len(twosec_samesrv_connections)
        srv_serror_count = 0
        srv_rerror_count = 0
        srv_diff_host_count = 0

        for cmprec in twosec_samesrv_connections:
            if rec.dst_ip != cmprec.dst_ip:
                srv_diff_host_count = srv_diff_host_count + 1
            if cmprec.flag == 'S0':
                srv_serror_count = srv_serror_count + 1
            elif cmprec.flag == 'REJ':
                srv_rerror_count = srv_rerror_count + 1

        srv_serror_rate = round(srv_serror_count / srv_count, 2)
        srv_rerror_rate = round(srv_rerror_count / srv_count, 2)
        srv_diff_host_rate = round(srv_diff_host_count / srv_count, 2)
        rec.add_sameservice_timebased_features(srv_count, srv_serror_rate,
                                               srv_rerror_rate, srv_diff_host_rate)

        # ---------------------------------------------------------------------
        # Derive host-based traffic features (same host over 100 connections)
        #  ---------------------------------------------------------------------
        for cmprec in samehost_connections:
            break


# pass control to collect_connections(), take all the credit
if __name__ == '__main__':
    if len(argv) == 2:
        pcap_file = argv[1]
    elif len(argv) == 1:
        pcap_file = 'sniff.pcap'
    else:
        exit("usage: python3 collect.py <input.pcap>")

    if not path.exists(pcap_file):
        exit("PCAP file not found: " + pcap_file)
    if not path.isfile(pcap_file):
        exit("Not a File: " + pcap_file)
    if pcap_file.lower().endswith('.pcap'):
        collect_connections(pcap_file)
        print('\nConnection records generated, written to records.csv\n')
