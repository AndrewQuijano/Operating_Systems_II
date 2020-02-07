#!/usr/bin/python

# --------------------------------------------------------------
#   Network Packet Sniffer:
#       a packet preprocessor that reads raw PCAP packet data,
#           aggregates packets into connection records, and
#           extracts/derives various features of the connections
#           consistent with those of the KDD CUP 99 dataset.
#
#    Authors: Daniel Mesko
#    Modified by: Andrew Quijano
# --------------------------------------------------------------


import pyshark
from sys import argv

# GLOBAL TODO:
#  - NEED TO DERIVE 100 connection window features
#  - Remove to_string pretty printers for packet/connection?


# An object for representing a single connection, with connection-based
# features as members
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

    def add_same_host_time_based_features(self, count, serror_rate, rerror_rate, same_srv_rate, diff_srv_rate):
        self.count = count
        self.serror_rate = serror_rate
        self.rerror_rate = rerror_rate
        self.same_srv_rate = same_srv_rate
        self.diff_srv_rate = diff_srv_rate

    def add_same_service_time_based_features(self, srv_count, srv_serror_rate,
                                           srv_rerror_rate, srv_diff_host_rate):
        self.srv_count = srv_count
        self.srv_serror_rate = srv_serror_rate
        self.srv_rerror_rate = srv_rerror_rate
        self.srv_diff_host_rate = srv_diff_host_rate

    def add_host_based_features(self, dst_host_count):
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
                   str(self.srv_diff_host_rate) + ',') + '\n'
        return out_str


# input: PCAP capture file
# output: full dictionary of Connection ID to Connection
def create_connection_records(cap):
    # ----------------------------------------------------------------
    # Collect packets from the same connection, create connection dict
    # ----------------------------------------------------------------
    raw_connections = {}
    udp_count = 0
    icmp_count = 0

    for packet in cap:
        try:
            if 'tcp' in packet:
                key = "tcp_conn" + packet.tcp.stream
            elif 'udp' in packet:
                key = "udp_conn" + str(udp_count)
                udp_count = udp_count + 1
            elif 'icmp' in packet:
                key = "icmp_conn" + str(icmp_count)
                icmp_count = icmp_count + 1
            else:
                # do not record packets that aren't TCP/UDP/ICMP
                continue

            # If the packet not in a connection record, make a new one!
            if key not in raw_connections.keys():
                raw_connections[key] = [packet]
            else:
                lst = raw_connections[key]
                lst.append(packet)

        except AttributeError:
            print("Attribute error found!")
            continue
    print('Connections found: ' + str(len(raw_connections)))
    return raw_connections


def initialize_connection(raw_connections):
    connections = []

    for key, packet_list in raw_connections.items():
        # TODO: does taking service layer of first packet always represent the connection accurately? I think not...
        src_bytes = 0
        dst_bytes = 0
        wrong_frag = 0
        urgent = 0
        if 'tcp' in packet_list[0]:
            protocol = 'TCP'
            duration = float(packet_list[-1].tcp.time_relative)
            src_port = packet_list[0].tcp.srcport
            dst_port = packet_list[0].tcp.dstport
        elif 'udp' in packet_list[0]:
            protocol = 'UDP'
            duration = float(packet_list[-1].udp.time_relative)
            src_port = packet_list[0].udp.srcport
            dst_port = packet_list[0].udp.dstport
        else:
            protocol = 'ICMP'
            duration = float(packet_list[-1].icmp.time_relative)
            src_port = packet_list[0].icmp.srcport
            dst_port = packet_list[0].icmp.dstport
        service = packet_list[0].highest_layer
        duration = int(duration / 1.0)
        src_ip = packet_list[0].ip.src
        dst_ip = packet_list[0].ip.dst
        timestamp = packet_list[-1].sniff_timestamp

        # land feature loop-back connection
        if src_ip == dst_ip and src_port == dst_port:
            land = 1
        else:
            land = 0

        # traverse packets (some basic features are aggregated from each packet)
        for packet in packet_list:
            if src_ip == packet.ip.src:
                src_bytes += int(packet.length.size)
            else:
                dst_bytes += int(packet.length.size)

            if protocol == 'TCP':
                if packet.tcp.flags_urg == 1:
                    urgent += 1
            if protocol == 'UDP':
                if packet.udp.flags_urg == 1:
                    urgent += 1
            if protocol == 'ICMP':
                if packet.icmp.flags_urg == 1:
                    urgent += 1

        status_flag = get_connection_status(packet_list)
        # ALSO....wrong fragments bit, hard-coding as 0

        # generate Connection with basic features as a tuple

        # Be sure to pre-prend: ip src, ip dst, time stamp
        # use a tuple so it can be sorted by timestamp and then by IP at the end!
        record = Connection(timestamp, src_ip, src_port, dst_ip, dst_port,
                            duration, protocol, service, 0, status_flag, src_bytes,
                            dst_bytes, land, 0, urgent)

        connections.append(record)

        # Write it out
        with open(str(key) + ".log", "w") as dummy:
            dummy.write(record.to_string())
            dummy.flush()

    # sort in terms of time! So you can easily find two last 2 seconds and last 100
    return sorted(connections, key=lambda x: x[0])


# Please view graph on main github page
def get_connection_status(packets):
    # define source and destination
    source_ip = packets[0].ip.src
    dest_ip = packets[0].ip.dst
    connection_status = 'SF'
    for packet in packets:
        if 'tcp' in packet:
            print(dir(packet.tcp))
            if packet.tcp.flags_syn == 1 and packet.ip.src == source_ip:
                connection_status = 'S0'
                # Reset is hit
                if packet.tcp.flags_reset == 1 and packet.ip.src == source_ip:
                    connection_status = 'REJ'
                    return connection_status
                elif packet.tcp.flags_reset == 1 and packet.ip.dest == dest_ip:
                    connection_status = 'RST0S0'
                    return connection_status
                # normal TCP handshake, SYN and ACK
                if packet.tcp.flags_syn == 1 and packet.tcp.flags_ack == 1:
                    connection_status = 'S1'

            elif packet.tcp.flags_fin == 1 and packet.ip.src == source_ip:
                connection_status = 'SH'
                return connection_status
            elif packet.tcp.flags_syn == 1 and packet.tcp.flags_ack == 1:
                connection_status = 'S4'
            else:
                connection_status = 'OTH'
                return connection_status

        elif 'udp' in packet:
            return 'SF'
        elif 'icmp' in packet:
            return 'SF'
        else:
            return 'ERROR'


# Derive time-based traffic features (over 2 sec window by default)
# Do this just for ONE connection!
def derive_time_features(connections, time_window=2.0):

    for rec in connections:
        samehost_connections = []
        twosec_samehost_connections = []
        twosec_samesrv_connections = []

        # traverse all connections to find same host, same service
        for cmprec in connections:
            time_delta = float(rec.timestamp) - float(cmprec.timestamp)
            if rec.dst_ip == cmprec.dst_ip:
                samehost_connections.append(cmprec)
                if (time_delta <= time_window) and (time_delta >= 0.0):
                    twosec_samehost_connections.append(cmprec)

            if rec.service == cmprec.service:
                if (time_delta <= time_window) and (time_delta >= 0.0):
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
            # TODO: do syn errors, rej errors

        same_srv_rate = round(same_srv_count / count, 2)
        diff_srv_rate = round(diff_srv_count / count, 2)
        rec.add_samehost_timebased_features(count, None, None,
                                            same_srv_rate, diff_srv_rate)

        # process two second same service connections
        srv_countcount = len(twosec_samesrv_connections)
        srv_serror_count = 0
        srv_rerror_count = 0
        srv_diff_host_count = 0

        for cmprec in twosec_samesrv_connections:
            if rec.dst_ip != cmprec.dst_ip:
                srv_diff_host_count = srv_diff_host_count + 1
            else:
                continue

            # TODO: do syn errors, rej errors

        srv_diff_host_rate = round(srv_diff_host_count / count, 2)
        rec.add_sameservice_timebased_features(count, None, None, srv_diff_host_rate)


def derive_host_features(connection, hosts=100):
    return


# the main function
def collect_connections(input_file):
    # Read in the file
    capture = pyshark.FileCapture(input_file)
    # Have a dictionary mapping of connection number to packets within connection
    raw_connections = create_connection_records(capture)

    # -------------------------------------------------------------------------
    # Derive basic features of each connection, create Connection objects list
    # -------------------------------------------------------------------------
    connections = initialize_connection(raw_connections)

    # Derive Time and Host Computations!
    connection_record_counter = 0
    for connection_record in connections:
        # ---------------------------------------------------------------------
        # Derive time-based traffic features (over 2 sec window)
        # ---------------------------------------------------------------------
        # same-host AND same-service feature derivation
        derive_time_features(connections)

        # ---------------------------------------------------------------------
        # Derive host-based traffic features (same host over 100 connections)
        #  ---------------------------------------------------------------------
        derive_host_features(connections)
        connection_record_counter += 1
        print("Completed Connection Record: " + str(connection_record_counter))

    # ---------------------------------------------------------------------
    # Traverse Connection list, generate CSV file
    # ---------------------------------------------------------------------
    with open('records.csv', 'w') as output:
        for rec in connections:
            output.write(rec.to_csv())
            output.flush()


# Label Encoder
# THIS IS FOR LABELING TEST DATA GENERATED BY THE FUZZER!
# THE OUTPUT OF KDD-PROCESSOR 99 -E Spits last 5 extra columns...
# SRC IP, SRC PORT, DEST IP, DEST PORT, TIME STAMP
# SINCE U KNOW THE ATTACKS ARE BY SPECIFIC IP, USE THAT TO LABEL
# PLAY WITH COLUMN 28-32
# GOAL: LABEL IS ON FIRST COLUMN
def label_testing_set(file_path, output):
    # From fuzzer I know the mapping of IP and attack
    # 192.168.147.152 is IP of Client running Kali Linux
    attack_map = {"192.168.147.150": "back.", "192.168.147.151": "neptune.",
                  "192.168.147.152": "satan.", "192.168.147.153": "teardrop.", "192.168.147.154": "pod.",
                  "192.168.147.160": "ipsweep.", "192.168.147.161": "portsweep.", "192.168.147.162": "portsweep."}
    # Pulled from NSL-KDD Labels
    label_map = {"normal.": 11, "back.": 0, "ipsweep.": 5, "land.": 6, "neptune.": 9, "pod.": 14,
                 "portsweep.": 15, "satan.": 17, "smurf.": 18, "teardrop.": 20}

    with open(file_path, "r") as read, open(output, "w+") as write:
        for line in read:
            ln = line.rstrip()
            parts = ln.split(',')

            # signature of land
            if parts[28] == parts[30]:
                parts.insert(0, str(label_map["land."]))
            elif parts[28] in attack_map:
                lab = attack_map[parts[28]]
                parts.insert(0, str(label_map[lab]))
            elif parts[30] in attack_map:
                lab = attack_map[parts[30]]
                parts.insert(0, str(label_map[lab]))
            else:
                parts.insert(0, str(label_map["normal."]))

            # drop the columns and write
            parts = parts[:29]
            new_line = ','.join(parts)
            write.write(new_line + '\n')
            write.flush()


def main():
    if len(argv) == 2:
        cap_file = argv[1]
        collect_connections(cap_file)
        print('Connection records generated, written to records.csv!')
    else:
        print('Usage: python3 kdd99_preprocessor.py <pcap-file>')


# The service mapping to port number is determined by IANA:
def get_iana():
    csv_location = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'


# pass control to collect_connections(), take all the credit
if __name__ == '__main__':
    main()
