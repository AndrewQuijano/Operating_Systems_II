# These attacks are designed to crack files that exist on the local host already
# Therefore, it is probably best for the sake of the program to have a thread attempt
# to break the following kind of files on local host
# 1- .pdf
# 2- .zip
from threading import Thread
from zipfile import ZipFile, BadZipFile
from pikepdf import open as PdfFileReader
from crypt import crypt


# Here is the .zip file cracker
# the input is a .zip file with password protection
def extract_file(zip_file, password):
    try:
        ZipFile(zip_file).extractall(pwd=password.encode('cp850', 'replace'))
        return True
    except BadZipFile:
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


def crack_zip_thread(zip_file, file="password.txt"):
    t = Thread(target=crack_zip_file(), args=(zip_file, file))
    t.start()


# Here is the .pdf file cracker. The input
# is a .pdf file with password protection
def extract_pdf(pdf, password):
    try:
        with open(pdf, "rb") as input_file:
            PdfFileReader(input_file, password)
            return True
    except PdfFileReader.PasswordError:
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


def crack_pdf_thread(pdf_file, file="password.txt"):
    t = Thread(target=crack_pdf_file(), args=(pdf_file, file))
    t.start()


# Assuming you have the /etc/shadow file, you can use this method
# to obtain the passwords of all users found in that file
def crack_local_host(crypt_pass, file="password.txt"):
    with open(file) as fd:
        for word in fd:
            if '#' in word:
                continue
            word = word.strip('\n')
            print(word)
            salt = crypt_pass[3:12]
            passwd = crypt(word, '$6$' + salt)
            if passwd == crypt_pass:
                print("[+] Found Password: " + word)
                return
    print("Password Not Found!")


def crack_local_thread(pass_file, file="password.txt"):
    t = Thread(target=crack_local_host(), args=(pass_file, file))
    t.start()
