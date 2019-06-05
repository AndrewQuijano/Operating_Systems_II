#!/usr/bin/python3
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from subprocess import call, run
from os import name
from os.path import basename, dirname, abspath

# The purpose of this class is mostly to modify data sets
# for machine learning purposes. This includes functions such
# as getting number of rows/columns, removing similar tuples and columns, etc.


# For kdd, we skip columns 10 - 22
# In our version, the label is in 0, so don't drop that!
# Input: file is the CSV file to be modified
# Input: ranges is a list of tuples containing columns to NOT be dropped!
def drop_columns(file_name, ranges, head=False):
    p = dirname(abspath(file_name))
    b = basename(file_name)
    use_cols = []
    for tup in ranges:
        use_cols = use_cols + [i for i in range(tup[0], tup[1])]
    df = pd.read_csv(file_name, usecols=use_cols)
    # Detect if Windows
    if name == 'nt':
        df.to_csv(p + "\\filtered_" + b, index=False, header=head)
    # Assume Linux otherwise
    else:
        df.to_csv(p + "/filtered_" + b, index=False, header=head)


# Remember Github's Limit is 100 MB or 100,000 KB
# So to store large datasets, I just split them up by 500,000 row chunks
def split_csv(file_name, size=500000):
    b = basename(file_name)
    p = dirname(abspath(file_name))
    file_part = 1
    idx = 1
    lines = []
    with open(file_name, 'r') as big_file:
        for line in big_file:
            if file_part % size == 0:
                if name == 'nt':
                    with open(p + "\\" + b + "_part_" + str(idx), 'w+') as chunk:
                        chunk.writelines(lines)
                else:
                    with open(p + "\\" + b + "_part" + str(idx), 'w+') as chunk:
                        chunk.writelines(lines)
                lines = []
                idx += 1
            else:
                lines.append(line)
            file_part += 1


# If you have
# ./kddcup_part1.csv, ./kddcup_part2.csv, kddcup_part3.csv, ...
# your file_name = ./kddcup.csv
# Assumes the parts will be in same directory as reassembled kddcup.csv!
def merge_csv(file_name, n_parts=9):
    b = basename(file_name)
    p = dirname(abspath(file_name))
    # Remove extension!
    b_part = b.split(".")
    b_part = str(b_part[0])
    file_part = 1
    # if n_parts is 9
    # j goes from 0 - 8
    # Remember files parts is goes 1 - 9!
    for j in range(n_parts):
        if name == 'nt':
            with open(p + "\\" + b_part + "_part" + str(j + 1) + ".csv", 'r') as chunk:
                with open(file_name, 'a+') as big_file:
                    for line in chunk:
                        big_file.write(line)
        else:
            with open(p + "/" + b_part + "_part" + str(j + 1) + ".csv", 'r') as chunk:
                with open(file_name, 'a+') as big_file:
                    for line in chunk:
                        big_file.write(line)
        file_part += 1


# Method drops a row if a certain column has a certain element
# anomaly,0,1,0
# normal,1,2,0
# If you want to remove anything in first column with normal.
# Use the method below
def drop_rows(file_name, to_drop, col_number):
    b = basename(file_name)
    p = dirname(abspath(file_name))
    counter = 0
    with open(file_name, "r") as fd, open(p + "\\drop_" + b, "w+") as wr:
        for line in fd:
            line = line.rstrip()
            args = line.split(',')
            if args[col_number] == to_drop:
                counter += 1
            else:
                wr.write(line + '\n')
                wr.flush()
    print("Number of " + to_drop + " found and dropped is: " + str(counter))


def unique_features(file_name, col_number):
    s = set()
    with open(file_name, "r") as read:
        for line in read:
            args = line.rstrip().split(",")
            s.add(args[col_number])
    return list(s)


# Given a file and list of columns to encode, this will take care of that.
def kdd_prep_2(file_name, to_encode, col_drop=None, shift=True):
    encoders = []
    for col in to_encode:
        features = unique_features(file_name, col)
        lab = LabelEncoder()
        lab.fit(features)
        encoders.insert(col, lab)
        label = lab.transform(features)
        with open("./labels.txt", "w") as f:
            f.write("For Column " + str(col))
            for k, v in features, label:
                f.write(k + "," + str(v) + '\n')
            f.write('\n')

    with open(file_name) as read_kdd_data, open("./kddcup_prep.csv", "w") as write_kdd:
        for line in read_kdd_data:
            # Swap using encoder
            line = line.rstrip()
            parts = line.split(",")
            # Starting from 0..
            # I must edit Column 1, 2, 3, 41
            for c in to_encode:
                parts[c] = str(encoders[c].transform(parts[c]))

            # Personally, I like my classes on first column not last
            if shift:
                last_column = parts[len(parts) - 1]
                parts.remove(parts[len(parts) - 1])
                parts.insert(0, last_column)

            # Check if you want to drop columns
            if col_drop is not None:
                for column in col_drop:
                    parts.remove(column)

            # Write the result
            new_line = ','.join(parts)
            write_kdd.write(new_line + '\n')
            write_kdd.flush()


def kdd_prep(file_name):
    # I know that there are some features that need to be encoded
    services = LabelEncoder()
    flags = LabelEncoder()
    protocol_type = LabelEncoder()

    # Have list of stuff
    proto = ["tcp", "udp", "icmp"]
    fl = ["SF", "S2", "S1", "S3", "OTH", "REJ", "RSTO", "S0", "RSTR", "RSTOS0", "SH"]
    serv = ["http", "smtp", "domain_u", "auth", "finger", "telnet", "eco_i", "ftp", "ntp_u",
            "ecr_i", "other", "urp_i", "private", "pop_3", "ftp_data", "netstat", "daytime", "ssh",
            "echo", "time", "name", "whois", "domain", "mtp", "gopher", "remote_job", "rje", "ctf",
            "supdup", "link", "systat", "discard", "X11", "shell", "login", "imap4", "nntp", "uucp",
            "pm_dump", "IRC", "Z39_50", "netbios_dgm", "ldap", "sunrpc", "courier", "exec", "bgp",
            "csnet_ns", "http_443", "klogin", "printer", "netbios_ssn", "pop_2", "nnsp", "efs",
            "hostnames", "uucp_path", "sql_net", "vmnet", "iso_tsap", "netbios_ns", "kshell",
            "urh_i", "http_2784", "harvest", "aol",
            "tftp_u", "http_8001", "tim_i", "red_i"]

    # Fit them with the known classes
    protocol_type.fit(proto)
    flags.fit(fl)
    services.fit(serv)
    proto_hat = protocol_type.transform(proto)
    fl_hat = flags.transform(fl)
    serv_hat = services.transform(serv)

    # Build dictionary!
    encode_protocol = dict(zip(proto, proto_hat))
    encode_fl = dict(zip(fl, fl_hat))
    encode_service = dict(zip(serv, serv_hat))
    with open("./labels.txt", "w") as f:
        for k, v in encode_protocol.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_fl.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_service.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')

    with open(file_name) as read_kdd_data, open("./kddcup_prep.csv", "w") as write_kdd:
        for line in read_kdd_data:
            # Swap using encoder
            line = line.rstrip()
            parts = line.split(",")
            # Starting from 0..
            # I must edit Column 1, 2, 3, 41
            parts[1] = str(encode_protocol[parts[1]])
            parts[2] = str(encode_service[parts[2]])
            parts[3] = str(encode_fl[parts[3]])

            # SHIFT COLUMN!
            # As my ML stuff excepts class on first column
            last_column = parts[len(parts) - 1]
            parts.remove(parts[len(parts) - 1])
            parts.insert(0, last_column)

            # As my ML stuff excepts class on first column
            new_line = ','.join(parts)
            write_kdd.write(new_line + '\n')
            write_kdd.flush()
    print("KDD Label encoding complete!")


# A decent chunk of data sets prefer the class to be the last column
# Personally, I prefer it to be the first column. This method will adjust that for me
def shift_column(file_name):
    with open(file_name) as read_kdd_data, open("./kddcup_swap.csv", "w") as write_kdd:
        for line in read_kdd_data:
            # Swap using encoder
            line = line.rstrip()
            parts = line.split(",")
            # As my ML stuff excepts class on first column
            last_column = parts[len(parts) - 1]
            parts.remove(parts[len(parts) - 1])
            parts.insert(0, last_column)
            # Write the result
            new_line = ','.join(parts)
            write_kdd.write(new_line + '\n')
            write_kdd.flush()


def n_col(file_name):
    col = -1
    with open(file_name) as read_data:
        for line in read_data:
            line = line.rstrip()
            parts = line.split(",")
            col = len(parts)
            if col > 0:
                break
    return col


def n_row(file_name):
    rows = 0
    with open(file_name) as data:
        for line in data:
            if line is not None:
                rows += 1
    return rows


def pcap(file_path, new_file=None):
    file_name = basename(file_path)
    file_parts = file_name.split('.')
    run(["sudo", "apparmor_parser", "-R", "/etc/apparmor.d/usr.sbin.tcpdump"])
    if new_file is not None:
        call(["tcpdump", "-r", file_path, "-w", new_file])
    else:
        call(["tcpdump", "-r", file_path, "-w", str(file_parts[0]) + ".pcap"])


def process(file_name, new_file=None):
    p = dirname(abspath(file_name))
    file_name = basename(file_name)
    if new_file is None:
        with open(p + "\\" + str(file_name.split(".")[0]) + ".csv", "w") as f:
            call(["sudo", "./kdd99extractor", file_name], stdout=f)
    else:
        with open(new_file, "w") as f:
            call(["sudo", "./kdd99extractor", file_name], stdout=f)


def build_kdd():
    # if geteuid() != 0:
    #    print("Need root permission!")
    #    exit(0)

    with open("./build_kdd.txt", "r") as f:
        for line in f:
            args = line.split()
            if args[0] == "pcap" and len(args) == 3:
                pcap(args[1], args[2])
            elif args[0] == "process" and len(args) == 3:
                process(args[1], args[2])
    print("Complete conversion to PCAP!")

    for i in range(35):
        process("kdd_" + str(i + 1) + ".pcap")
    merge_csv("kdd", n_parts=35)


# Filter out any tuples that are duplicates
# Used in NSL-KDD as it filters duplicates from KDD-Cup 1999
def filter_duplicate(original_file, new_file):
    s = set()
    with open(original_file) as read_kdd_data:
        for line in read_kdd_data:
            # Swap using encoder
            line = line.rstrip()
            s.add(line)

    # Print new data set
    with open(new_file, "w+") as write_kdd:
        for row in s:
            write_kdd.write(row + '\n')


def compare_csv(file_1, file_2):
    size = 0
    similarity = 0
    with open(file_1, "r") as read_kdd_data, open(file_2, "r") as read_nsl_data:
        for kdd_line, nsl_line in read_kdd_data, read_nsl_data:
            if kdd_line == nsl_line:
                similarity = similarity + 1
            size = size + 1
    return similarity/size


# To convert KDD
# 1- First Swap columns AND Encode it
# 2- Drop Columns that are content related
# 3- Split into parts -- FOR SAVING IT ONLY
# **To use it, just merge it, use raw file name w/o extension!**
if __name__ == "__main__":
    drop_columns("./kddcup.csv", [(0, 9), (21, 42)])
    # kdd_prep("kddcup.csv")
    # drop_columns("kddcup_prep.csv")
    # split_csv("modified_kddcup_prep.csv")
    # build_kdd()
    # nsl_kdd_filter("kdd.csv")
    # n_row("kdd.csv")
    # n_row("NSL_KDD.csv")
    # compare_csv("kdd.csv", "NSL_KDD.csv")
