import socket
from sys import exit


def die(message):
    print(message)
    exit(0)


def create_server_socket(port_number, max_connections=5):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('', port_number))
    except socket.error:
        if server_socket:
            server_socket.close()
        return None
    server_socket.listen(max_connections)  # Now wait for client connection.
    return server_socket


def valid_ip(ip):
    test = ip.split('.')
    if len(test) != 4:
        return False
    try:
        for i in range(len(test)):
            if int(test[i]) < 0 or int(test[i]) > 255:
                return False

    except ValueError:
        return False
    return True


def valid_port(port):
    try:
        port_number = int(port)
    except ValueError:
        return False
    if port_number <= 1024:
        return False
    elif port_number > 65535:
        return False
    return True
