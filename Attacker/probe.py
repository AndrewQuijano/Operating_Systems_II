# https://thepacketgeek.com/scapy-p-10-emulating-nmap-functions/
# Above is a cool link for linking more nmap with scapy
# But as seen above, it is just fancier code for scanning stuff....
from scapy.all import *


# Matches most with IPSWEEP
def ping(ping_target="127.0.0.1", time_out=3, src_ip="192.168.147.160", naive=True):
    print("Start basic ping...")
    if naive:
        answer = sr1(IP(src=src_ip, dst=ping_target)/ICMP()/b"XXXXXXXXXXX", timeout=time_out)
    else:
        answer = sr1(IP(src=src_ip, dst=ping_target) / ICMP() / b"XXXXXXXXXXX", timeout=time_out, inter=1)
    if answer is not None:
        answer.show()
    else:
        print("[Ping] No answer at:" + ping_target)
    return answer


# Return a Dictionary of <IP Address, Open Port>
# Matches most with PORTSWEEP
def host_scan(host, min_port=1024, max_port=65535, time_out=3, src_ip="192.168.147.161", naive=True):
    print("Start Host Scan...")
    # Use TCP with SYN flag to look
    if naive:
        ans, unans = sr(IP(src=src_ip, dst=host)/TCP(dport=range(min_port, max_port), flags="S"), timeout=time_out)
    else:
        ans, unans = sr(IP(src=src_ip, dst=host) / TCP(dport=range(min_port, max_port), flags="S"), timeout=time_out,
                        inter=1)

    # Use TCP with ACK flag to look
    if naive:
        ans, unans = sr(IP(src=src_ip, dst=host)/TCP(dport=range(min_port, max_port), flags="A"), timeout=time_out)
    else:
        ans, unans = sr(IP(src=src_ip, dst=host) / TCP(dport=range(min_port, max_port), flags="A"), timeout=time_out,
                        inter=1)
    print("Host Scan complete...")


# UDP Ping
# If all else fails there is always UDP Ping which will produce ICMP Port unreachable errors
# from live hosts. Here you can pick any port which is most likely to be closed,
# such as port 0:
# Matches most with PORTSWEEP
def udp_ping(host, min_port=0, max_port=65535, time_out=3, src_ip="192.168.147.162", naive=True):
    print("UDP scan of all ports...")
    if naive:
        ans, unans = sr(IP(src=src_ip, dst=host) / UDP(dport=range(min_port, max_port)), timeout=time_out)
    else:
        ans, unans = sr(IP(src=src_ip, dst=host) / UDP(dport=range(min_port, max_port)), timeout=time_out,
                        inter=1)
    print("UDP Scan complete...")


# ARP-Ping
def arp_ping(network="192.168.147.0/24", time_out=2):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), timeout=time_out, verbose=False)
    ans_list = list(ans)
    for a in ans_list:
        print(a)
