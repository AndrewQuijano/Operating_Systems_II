import pandas as pd
from sklearn.preprocessing import LabelEncoder


# For kdd, we skip columns 10 - 22
# In our version, the label is in 0, so don't drop that!
def drop_columns(file, begin=0, end=9, begin_2=23, end_2=42):
    range1 = [i for i in range(begin, end)]
    range2 = [i for i in range(begin_2, end_2)]
    use_cols = range1 + range2
    df = pd.read_csv(file, usecols=use_cols)
    df.to_csv("modified_" + file, index=False, header=False)


# Remember Github's Limit is 100 MB or 100,000 KB
def split_csv(file, size=500000):
    file_part = 0
    idx = 0
    lines = []
    with open(file, 'r') as big_file:
        for line in big_file:
            if file_part % size == 0:
                with open(str(idx) + "_" + str(file), 'w+') as chunk:
                    chunk.writelines(lines)
                lines = []
                idx += 1
            else:
                lines.append(line)
            file_part += 1


def merge_csv(file):
    file_part = 1
    for j in range(9):
        with open(str(file_part) + "_" + file + ".csv", 'r') as chunk:
            with open(file + ".csv", 'a+') as big_file:
                for line in chunk:
                    big_file.write(line)
        file_part += 1


# For QDA it requires one class with only one sample be dropped? Find it and kill it!
def drop_class(file, drop):
    counter = 0
    with open(file, "r") as fd, open("n_" + file, "w") as wr:
        for line in fd:
            line = line.rstrip()
            args = line.split(',')
            if args[41] == drop:
                counter += 1
            else:
                print(line)
                wr.write(line + '\n')
                wr.flush()
    print("Number of " + drop + " found and dropped is: " + str(counter))


def kdd_prep(file):
    # I know that there are some features that need to be encoded
    classes = LabelEncoder()
    services = LabelEncoder()
    flags = LabelEncoder()
    protocol_type = LabelEncoder()

    # Have list of stuff
    y = ["normal.", "back.", "buffer_overflow.", "ftp_write.", "guess_passwd.",
                 "imap.", "ipsweep.", "land.", "loadmodule.", "multihop.", "neptune.",
                 "nmap.", "perl.", "phf.", "pod.", "portsweep.", "rootkit.", "satan.", "smurf.",
                 "spy.", "teardrop.", "warezclient.", "warezmaster."]
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
    classes.fit(y)
    protocol_type.fit(proto)
    flags.fit(fl)
    services.fit(serv)
    y_hat = classes.transform(y)
    proto_hat = protocol_type.transform(proto)
    fl_hat = flags.transform(fl)
    serv_hat = services.transform(serv)

    # Build dictionary!
    encode_class = dict(zip(y, y_hat))
    encode_protocol = dict(zip(proto, proto_hat))
    encode_fl = dict(zip(fl, fl_hat))
    encode_service = dict(zip(serv, serv_hat))
    with open("./labels.txt", "w") as f:
        for k, v in encode_class.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_protocol.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_fl.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_service.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')

    with open(file) as read_kdd_data, open("./kddcup_prep.csv", "w") as write_kdd:
            for line in read_kdd_data:
                # Swap using encoder
                line = line.rstrip()
                parts = line.split(",")
                # Starting from 0..
                # I must edit Column 1, 2, 3, 41
                parts[1] = str(encode_protocol[parts[1]])
                parts[2] = str(encode_service[parts[2]])
                parts[3] = str(encode_fl[parts[3]])
                parts[41] = str(encode_class[parts[41]])
                # As my ML stuff excepts class on first column
                swap_positions(parts, 0, 41)
                new_line = ','.join(parts)
                write_kdd.write(new_line + '\n')
                write_kdd.flush()
    print("KDD Label encoding complete!")


def swap_positions(l, pos1, pos2):
    l[pos1], l[pos2] = l[pos2], l[pos1]
    return l


# To convert KDD
# 1- First encode
# 2- Drop Columns
# 3- Split into parts
# **To use it, just merge it, use raw file name w/o extension!**
if __name__ == "__main__":
    drop_class("kddcup.csv", "imap.")
    # kdd_prep("kddcup.csv")
    # drop_columns("kddcup_prep.csv")
    # split_csv("modified_kddcup_prep.csv")
    # merge_csv("kddcup")
