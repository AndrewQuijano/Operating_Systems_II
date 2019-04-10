# !/usr/bin/env python3
# Andrew Quijano
# UNI: afq2101
from pathlib import Path


def valid_ip(ip):
    try:
        test = ip.split('.')
        if len(test) != 4:
            return False

        for i in range(len(test)):
            if int(test[i]) < 0 or int(test[i]) > 255:
                return False
    except ValueError:
        return False
    return True


def valid_port(port, dos=False):
    try:
        port_number = int(port)
    except ValueError:
        return False

    if dos:
        if port_number < 0:
            return False
        elif port_number > 65535:
            return False
    else:
        if port_number < 1024:
            return False
        elif port_number > 65535:
            return False
    return True


def valid_extension(file, ext):
    try:
        name = Path(file).name
        parts = name.split('.')
        if len(parts) != 2:
            return False
        else:
            if parts[1] == ext:
                return True
            else:
                return False
    except ValueError:
        return False
