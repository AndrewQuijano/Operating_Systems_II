from scapy.all import *


def ping(ping_target="127.0.0.1", time_out=5, src_ip="192.168.147.160"):
    answer = sr1(IP(src=src_ip, dst=ping_target)/ICMP()/b"XXXXXXXXXXX", timeout=time_out)
    if answer is not None:
        answer.show()
    else:
        print("No answer at:" + ping_target)
    return answer


# Return a Dictionary of <IP Address, Open Port>
def host_scan(host, min_port=1024, max_port=65535, time_out=2, src_ip="192.168.147.161"):
    # Use TCP with SYN flag to look
    ans, unans = sr(IP(src=src_ip, dst=host)/TCP(dport=range(min_port, max_port), flags="S"), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)

    # Use TCP with ACK flag to look
    ans, unans = sr(IP(src=src_ip, dst=host)/TCP(dport=range(min_port, max_port), flags="A"), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)


# UDP Ping
# If all else fails there is always UDP Ping which will produce ICMP Port unreachable errors
# from live hosts. Here you can pick any port which is most likely to be closed,
# such as port 0:
def udp_ping(host, min_port=0, max_port=65535, time_out=2, src_ip="192.168.147.162"):
    ans, unans = sr(IP(src=src_ip, dst=host) / UDP(dport=range(min_port, max_port)), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)


# ARP-Ping
def arp_ping(network, time_out=2):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)
