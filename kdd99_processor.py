#!/usr/bin/python

# --------------------------------------------------------------
#   Network Packet Sniffer:
#       a packet preprocessor that reads raw PCAP packet data,
#           aggregates packets into connection records, and
#           extracts/derives various features of the connections
#           consistent with those of the KDD CUP 99 dataset.
#
#    Author: Andrew Quijano
# --------------------------------------------------------------


import pyshark
import time
from sys import argv
# import urllib3


# input: Packet capture file
# output: full dictionary of Connection ID to all packets within the connection
def create_connection_records(cap):
    # ----------------------------------------------------------------
    # Collect packets from the same connection, create connection dict
    # ----------------------------------------------------------------
    raw_connections = {}
    # udp_count = 0
    icmp_count = 0

    # Start time
    start_time = start_time = time.time()

    for packet in cap:

        try:
            if 'tcp' in packet:
                key = "tcp_conn" + packet.tcp.stream
            elif 'udp' in packet:
                # key = "udp_conn" + str(udp_count)
                key = 'udp_conn' + packet.udp.stream
                # udp_count = udp_count + 1
            elif 'icmp' in packet:
                key = "icmp_conn" + str(icmp_count)
                icmp_count += 1
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
            continue
    print("--- %s seconds to collect connection records ---" % (time.time() - start_time))
    print('Connections found: ' + str(len(raw_connections)))
    return raw_connections


def ip_address_index(ip_address, ipv4=True):
    power = 0
    index = 0
    if ipv4:
        numeric_parts = ip_address.split('.')
        numeric_parts.reverse()
        for num in numeric_parts:
            index += int(num) * pow(10, power)
            power += 3
    else:
        # TODO: INDEX THIS???
        print(ip_address)
        index = 1
    return index


def initialize_connection(raw_connections):
    connections = []
    # Get the service name
    service_mapping = get_iana()
    # Know the index number so you can get the list index to save time
    idx = 0

    for key, packet_list in raw_connections.items():
        src_bytes = 0
        dst_bytes = 0
        wrong_frag = 0
        urgent = 0

        idx += 1
        if 'tcp' in packet_list[0]:
            protocol = 'tcp'
            duration = float(packet_list[-1].tcp.time_relative)
            src_port = int(packet_list[0].tcp.srcport)
            dst_port = int(packet_list[0].tcp.dstport)
            if src_port <= dst_port:
                service = service_mapping[('tcp', src_port)]
            else:
                service = service_mapping[('tcp', dst_port)]

        elif 'udp' in packet_list[0]:
            protocol = 'udp'
            duration = float(packet_list[-1].udp.time_relative)
            src_port = int(packet_list[0].udp.srcport)
            dst_port = int(packet_list[0].udp.dstport)
            if src_port <= dst_port:
                service = service_mapping[('udp', src_port)]
            else:
                service = service_mapping[('udp', dst_port)]
        elif 'icmp' in packet_list[0]:
            protocol = 'icmp'
            duration = float(packet_list[-1].icmp.time_relative)
            src_port = int(packet_list[0].icmp.srcport)
            dst_port = int(packet_list[0].icmp.dstport)
            # see ICMP.cc
            service = 'eco_i'
        else:
            continue

        duration = int(duration)

        # IPv4 and IPv6...
        if 'ip' in packet_list[0]:
            # IPv4
            src_ip = packet_list[0].ip.src
            dst_ip = packet_list[0].ip.dst
            index = ip_address_index(dst_ip)
            status_flag = get_connection_status(packet_list)
        else:
            # IPv6
            src_ip = packet_list[0].ipv6.src
            dst_ip = packet_list[0].ipv6.dst
            index = ip_address_index(dst_ip, False)
            status_flag = get_connection_status(packet_list, False)

        # land feature loop-back connection
        if src_ip == dst_ip and src_port == dst_port:
            land = 1
        else:
            land = 0

        timestamp = packet_list[-1].sniff_timestamp
        # traverse packets (some basic features are aggregated from each packet in whole connection)
        for packet in packet_list:
            if 'ip' in packet_list[0]:
                if src_ip == packet.ip.src:
                    src_bytes += int(packet.length.size)
                else:
                    dst_bytes += int(packet.length.size)
            else:
                if src_ip == packet.ipv6.src:
                    src_bytes += int(packet.length.size)
                else:
                    dst_bytes += int(packet.length.size)

            # Urgent packets only happen with TCP
            if protocol == 'tcp':
                if packet.tcp.flags_urg == '1':
                    urgent += 1
                if packet.tcp.checksum_status != '2':
                    wrong_frag += 1

            elif protocol == 'udp':
                if packet.udp.checksum_status != '2':
                    wrong_frag += 1

            elif protocol == 'icmp':
                if packet.icmp.checksum_status != '2':
                    wrong_frag += 1

        # generate Connection with basic features as a tuple
        # Be sure to prepend: ip src, ip dst, time stamp
        # use a tuple so it can be sorted by timestamp and then by IP at the end!
        record = (timestamp, src_ip, src_port, dst_ip, dst_port, index, idx,
                  duration, protocol, service, status_flag, src_bytes,
                  dst_bytes, land, wrong_frag, urgent)
        connections.append(record)
        print(record)
        get_content_data(packet_list)

    # sort in terms of time! So you can easily find two last 2 seconds and last 100
    return sorted(connections, key=lambda x: x[0])


# Please view graph on main github page
# Given a list of packets return connection status
# Here is tha link on how I implemented DFA
# https://stackoverflow.com/questions/35272592/how-are-finite-automata-implemented-in-code
def get_connection_status(packets, ipv4=True):

    if 'udp' in packets[0] or 'icmp' in packets[0]:
        return 'SF'

    # The terms needed are: Source -> Destination, SYN, ACK, RST, FIN
    # Judging by KDD data set, NO S2F or S3F was found
    conn = {'INIT': {('0', '1', '1', '0', '0'): 'S4', ('1', '0', '0', '0', '1'): 'SH', ('1', '1', '0', '0', '0'): 'S0'}, # OTH IS ACCOUNTED FOR
            'S4': {('0', '0', '0', '1', '0'): 'SHR', ('0', '0', '0', '0', '1'): 'RSTRH'},
            'SH': {},               # END NOW
            'SHR': {},              # END NOW
            'RSTRH': {},            # END NOW
            'OTH': {},              # END NOW
            'S0': {('0', '1', '1', '0', '0'): 'S1', ('0', '0', '0', '1', '0'): 'REJ', ('1', '0', '0', '1', '0'): 'RST0S0'},
            'REJ': {},              # END NOW
            'RST0S0': {},           # END NOW
            'RST0': {},             # END NOW
            'RSTR': {},             # END NOW
            'S1': {('1', '0', '1', '0', '0'): 'ESTAB', ('1', '0', '0', '1', '0'): 'RST0', ('0', '0', '0', '1', '0'): 'RSTR'},
            'ESTAB': {('1', '0', '1', '0', '1'): 'S2', ('0', '0', '1', '0', '1'): 'S3'},
            'S2': {('0', '0', '1', '0', '0'): 'SF'},
            'S3': {('1', '0', '1', '0', '0'): 'SF'},
            'SF': {}}                  # END NOW
    # Define source and destination
    if ipv4:
        source_ip = packets[0].ip.src
    else:
        source_ip = packets[0].ipv6.src
    connection_status = 'INIT'

    # Now you need the key in the DFA
    # The terms needed are: Source -> Destination, SYN, ACK, RST, FIN

    for packet in packets:
        if ipv4:
            if source_ip == packet.ip.src:
                key = ('1', packet.tcp.flags_syn, packet.tcp.flags_ack, packet.tcp.flags_reset, packet.tcp.flags_fin)
            else:
                key = ('0', packet.tcp.flags_syn, packet.tcp.flags_ack, packet.tcp.flags_reset, packet.tcp.flags_fin)
        else:
            if source_ip == packet.ipv6.src:
                key = ('1', packet.tcp.flags_syn, packet.tcp.flags_ack, packet.tcp.flags_reset, packet.tcp.flags_fin)
            else:
                key = ('0', packet.tcp.flags_syn, packet.tcp.flags_ack, packet.tcp.flags_reset, packet.tcp.flags_fin)

        # print("STATE IS NOW: " + connection_status)
        # print(key)
        try:
            connection_status = conn[connection_status][key]
        except KeyError:
            if connection_status == 'INIT':
                return 'OTH'
            elif connection_status == 'SH' or connection_status == 'SHR':
                return connection_status
            elif connection_status == 'RSTRH' or connection_status == 'OTH':
                return connection_status
            elif connection_status == 'REJ' or connection_status == 'RST0S0' or connection_status == 'RST0':
                return connection_status
            elif connection_status == 'RSTR' or connection_status == 'SF':
                return connection_status
            else:
                continue
    return connection_status


def get_content_data(packet_list):
    hot = 0
    num_failed_logins = 0
    logged_in = 0
    num_compromised = 0
    root_shell = 0
    su_attempted = 0
    num_root = 0
    num_file_creations = 0
    num_access_files = 0
    num_outbound_cmds = 0
    is_hot_login = 0
    is_guest_login = 0

    packet_no = 1
    for packet in packet_list:
        try:
            # Get the ASCII output
            byte_list = packet.tcp.payload.replace(':', '')
            commmand = bytes.fromhex(byte_list).decode()
            # print(packet_no)
            print(commmand, end="")

            # First check if for login attempt successful or not
            if logged_in == 1:
                # User is logged in, try to get the prompt!
                if '#' in commmand:
                    root_shell = 1
                if '$' or '#' in commmand:
                    # print(commmand, end='')
                    3 + 4
            else:
                # User is NOT logged in
                if 'Last login' in commmand:
                    logged_in = 1
                if 'failed' in commmand:
                    num_failed_logins += 1
            packet_no += 1
        except UnicodeDecodeError:
            continue
        except AttributeError:
            continue
    return (hot, num_failed_logins, logged_in, num_compromised, logged_in, num_compromised, root_shell,
            su_attempted, num_root, num_file_creations, num_access_files, num_outbound_cmds, is_hot_login,
            is_guest_login)


# Derive time-based traffic features (over 2 sec window by default)
# Do this just for ONE connection!
# I AM ASSUMING IT IS ALREADY SORTED BY TIMESTAMP!
def derive_time_features(connection_idx, connections, time_window=2.0):
    current_connection = connections[connection_idx]
    current_conn_time = current_connection[0]
    current_ip = current_connection[1]
    current_conn_service = current_connection[9]
    current_conn_status = current_connection[10]

    # Since it is sorted by time stamp, I just need to go backward!
    samehost_connections = []
    twosec_samehost_connections = []
    twosec_samesrv_connections = []
    counter = connection_idx - 1

    count = 0
    srv_count = 0
    serror_rate = 0
    srv_serror_rate = 0
    rerror_rate = 0
    srv_error_rate = 0
    same_srv_rate = 0
    diff_srv_rate = 0
    srv_diff_host_rate = 0

    # Step 1- Collect all relevant (service, flag) tuples
    while True:
        # Don't go out of bounds
        if counter < 0:
            break

        time_delta = float(current_conn_time) - float(connections[counter])
        if time_delta < time_window:
            break

        # Collect all connection data
        other_connection = connections[counter]

        if current_ip == other_connection[1]:
            samehost_connections.append('hi')

        if current_conn_service == other_connection[1]:
            twosec_samesrv_connections.append('hi')

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

    return (count, srv_count, serror_rate, srv_serror_rate, rerror_rate,
            srv_error_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate)


def derive_host_features(connection, hosts=100):
    return 'temp', 'hi'


# the main function
def collect_connections(input_file, keep_extra=False):
    # Read in the file
    capture = pyshark.FileCapture(input_file)
    # Have a dictionary mapping of connection number to packets within connection
    raw_connections = create_connection_records(capture)

    # -------------------------------------------------------------------------
    # Derive basic features of each connection, create Connection tuples list: Columns 1 - 11
    # -------------------------------------------------------------------------
    connections = initialize_connection(raw_connections)

    # Derive Time and Host Computations!
    connection_record_counter = 0
    for connection_record in connections:
        # ---------------------------------------------------------------------
        # Derive time-based traffic features (over 2 sec window)
        # ---------------------------------------------------------------------
        # same-host AND same-service feature derivation
        # time_traffic = derive_time_features(connection_record_counter, connections)

        # ---------------------------------------------------------------------
        # Derive host-based traffic features (same host over 100 connections)
        #  ---------------------------------------------------------------------
        # host_traffic = derive_host_features(connections)
        connection_record_counter += 1

        # Append the answers!
        # connection_record += time_traffic
        # connection_record += host_traffic
        print("Completed Connection Record: " + str(connection_record_counter))

    # ---------------------------------------------------------------------
    # Traverse Connection list, generate CSV file
    # ---------------------------------------------------------------------
    with open('kdd.csv', 'w+') as out:
        # delete the timestamp, src ip, src port, dest ip, dest port, dest_ip_idx, idx
        for record in connections:
            if keep_extra:
                out.write(','.join(list(record)) + '\n')
            else:
                filtered_line = list(record)[7:]
                filtered_line = ','.join([str(i) for i in filtered_line])
                out.write(filtered_line + '\n')


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
    if len(argv) == 1:
        # cap_file = './outside.tcpdump'
        cap_file = './test.pcap'
        # cap_file = './telnet.pcapng'
        collect_connections(cap_file)
    elif len(argv) == 2:
        cap_file = argv[1]
        collect_connections(cap_file)
        print('Connection records generated, written to records.csv!')
    else:
        print('Usage: python3 kdd99_preprocessor.py <pcap-file>')


# The service mapping to port number is determined by IANA:
# Return a dictionary of tcp/udp to port numbers
def get_iana():
    # Get the CSV file from HTTP
    # url = 'https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv'
    # user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'}
    # pool = urllib3.HTTPConnectionPool(url, maxsize=1, headers=user_agent, port=80)
    # response = pool.request('GET', url)

    # Open the CSV file
    service_mapping = {}
    filename = './service-names-port-numbers.csv'
    with open(filename, 'r') as fd:
        # Only get the first three columns
        for line in fd:
            stuff = line.split(',')
            try:
                service = stuff[0]
                port_protocol_tuple = (stuff[2], int(stuff[1]))
                if service == '' or stuff[1] == '' or stuff[2] == '':
                    continue
                else:
                    # Ensure the port is number!
                    # print(port_protocol_tuple)
                    # print(service)
                    service_mapping[port_protocol_tuple] = service
            except IndexError:
                continue
            except ValueError:
                continue
    # Manually enter port 80
    service_mapping[('tcp', 80)] = 'http'
    service_mapping[('udp', 80)] = 'http'
    return service_mapping


# pass control to collect_connections(), take all the credit
if __name__ == '__main__':
    main()
