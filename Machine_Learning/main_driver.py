#!/usr/bin/env python3
from bayes import *
from discriminant import *
from KNN import *
from logistic_regression import *
from random_forest import *
from svm import *
from decision_tree import *
from sys import argv, exit
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
import subprocess
import collections
from misc import read_data
from collections import OrderedDict
from operator import itemgetter
from joblib import load
from math import sqrt
from os.path import basename, dirname, abspath
from os import name


# Just test functionality of script!
def main():
    train_x = None
    train_y = None
    test_x = None
    test_y = None

    # Check if both sets are available
    if len(argv) == 2:
        # Read the training and testing data-set
        # This assumes the class variable is on the first column!
        # It also assumes all data is numeric!
        if is_valid_file_type(argv[1]):
            train_x, train_y = read_data(argv[1])
        else:
            print("Training Set Not Found or invalid file extension!")
            exit(0)

        # Now make a split between training and testing set from the input data
        train_x, train_y, test_x, test_y = get_cv_set(train_x, train_y)
        p = dirname(abspath(argv[1]))
        b = basename(argv[1])

        # Format columns to be 1-D shape
        train_y = train_y.reshape(-1, 1)
        test_y = test_y.reshape(-1, 1)
        train = np.concatenate((train_y, train_x), axis=1)
        test = np.concatenate((test_y, test_x), axis=1)

        if name == 'nt':
            np.savetxt(p + '\\train_' + b, train, fmt="%s", delimiter=",")
            np.savetxt(p + "\\test_" + b, test, fmt="%s", delimiter=",")
        else:
            np.savetxt(p + "/train_" + b, train, fmt="%s", delimiter=",")
            np.savetxt(p + "/test_" + b, test,  fmt="%s", delimiter=",")
        exit(0)

    elif len(argv) == 3:
        # Read the training and testing data-set
        # This assumes the class variable is on the first column!
        # It also assumes all data is numeric!
        if is_valid_file_type(argv[1]):
            train_x, train_y = read_data(argv[1])
        else:
            print("Training Set Not Found or invalid file extension!")
            exit(0)

        if is_valid_file_type(argv[2]):
            test_x, test_y = read_data(argv[2])
        else:
            print("Testing Set Not Found or invalid file extension!")
            exit(0)
    else:
        print("Usage: python3 main_driver <train-set> <test-set>")
        exit(0)

    # First thing, Check if there was a previous run or not!
    # Then the user chooses to delete and run or not
    start_and_clean_up()

    # Now train ALL classifiers!

    # 1- SVM
    start_time = time.time()
    # svm_line_clf = svm_linear(train_x, train_y, slow=True)
    # svm_rbf_clf = svm_rbf(train_x, train_y, slow=True)

    # 2- Random Forest
    # forest_clf = get_forest(train_x, train_y, slow=True)

    # 3- Neural Networks
    # brain_clf = get_brain(train_x, train_y)

    # 4- Logistic Regression
    # logit_clf = get_logistic(train_x, train_y, slow=True)

    # 5- KNN
    # knn_clf = get_knn(train_x, train_y, slow=True)

    # 6- LDA/QDA
    # lda_clf = discriminant_line(train_x, train_y)
    # qda_clf = discriminant_quad(train_x, train_y)

    # 7- Bayes
    # bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y)

    # 8- Decision Tree
    tree = get_tree(train_x, train_y, slow=False)
    tree = get_tree(train_x, train_y, slow=True)

    # Run Testing Now
    # svm_test(svm_line_clf, test_x, test_y, "Linear")
    # svm_test(svm_rbf_clf, test_x, test_y, "Radial")
    # forest_test(forest_clf, test_x, test_y)
    # log_linear_test(logit_clf, test_x, test_y)
    # knn_test(knn_clf, train_x, train_y)
    # lda_test(lda_clf, test_x, test_y)
    # qda_test(qda_clf, test_x, test_y)
    # naive_bayes_test(bayes, bayes_isotonic, bayes_sigmoid, test_x, test_y)
    tree_test(tree, test_x, test_y)
    # brain_test(brain_clf, test_x, test_y)
    print("---Time to complete training everything: %s seconds---" % (time.time() - start_time))


# Use this to run IDS using Classifier!
def ids():
    # To run the program I need either
    # 1- the raw PCAP with labels?
    # 2- just the raw CSV pre-processed using Stolfo's KDD Data mining techniques
    if len(argv) != 2:
        exit("usage: python3 main_ids <training data set>")
    # PCAP File not accepted for training!
    if not is_valid_file_type(argv[1]):
        exit("Invalid file type! only accept.txt or .csv file extensions!")

    print("Please wait...Reading the Training Data ML...")
    train_x, train_y = read_data(argv[1])
    print("Please wait...Training Data read! Setting up ML Models!")

    # Now make a split between training and testing set from the input data
    start_time = time.time()
    kf = KFold(n_splits=5, shuffle=False)

    # 1- Bayes
    print("Fitting Bayes Classifiers...")
    bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y, n_fold=kf)
    print("Bayes classifier ready!")

    # 2- LDA/QDA
    print("Fitting LDA and QDA...")
    lda_clf = discriminant_line(train_x, train_y)
    print("LDA ready!")

    qda_clf = discriminant_quad(train_x, train_y)
    print("QDA ready!")

    # 3- SVM
    print("Fitting Linear SVM...")
    svm_line_clf = svm_linear(train_x, train_y, n_fold=kf, slow=False)

    # print("SVM Linear Model Ready!")
    print("Fitting RBF SVM...")
    svm_rbf_clf = svm_rbf(train_x, train_y, n_fold=kf, slow=False)
    print("SVM RBF Kernel Ready!")

    # 4- Random Forest
    print("Fitting Random Forest...")
    forest_clf = get_forest(train_x, train_y, n_fold=kf, slow=False)
    print("Random Forest Ready!")

    # 5- Logistic Regression
    print("Fitting Logistic Regression...")
    logistic_clf = get_logistic(train_x, train_y, n_fold=kf, slow=False)
    print("Logistic Regression Ready!")

    # 6- KNN
    print("Fitting KNN...")
    knn_clf = get_knn(train_x, train_y, n_fold=kf, slow=False)
    print("KNN ready!")

    # 7- Decision Tree
    print("Fitting Decision tree...")
    tree = get_tree(train_x, train_y, n_fold=kf, slow=False)
    print("Decision tree ready!")

    print("--- Model Training Time: %s seconds ---" % (time.time() - start_time))
    print("All models are trained...")

    while True:
        try:
            # Read input from user
            arg = input("Input: ")
            args = arg.split()
            if args[0] == "exit":
                break
            # This argument is run the IDS with the test data
            elif args[0] == "detect":  # args: csv type
                # Check if the correct CSV file exists, if so read it in!
                if not is_valid_file_type(args[1]):
                    continue
                test_x, test_y = read_data(args[1])

                naive_bayes_test(bayes, bayes_isotonic, bayes_sigmoid, test_x, test_y)
                lda_test(lda_clf, test_x, test_y)
                qda_test(qda_clf, test_x, test_y)

                if svm_line_clf is not None:
                    svm_test(svm_line_clf, test_x, test_y, "Linear")
                if svm_rbf_clf is not None:
                    svm_test(svm_rbf_clf, test_x, test_y, "Radial")
                if forest_clf is not None:
                    forest_test(forest_clf, test_x, test_y)
                if logistic_clf is not None:
                    log_linear_test(logistic_clf, test_x, test_y)
                if knn_clf is not None:
                    knn_test(knn_clf, test_x, test_y)
                if tree is not None:
                    tree_test(tree, test_x, test_y)

            # Bring new ML model!
            elif args[0] == "tune":
                if args[1] == "line_svm":
                    print("Fitting Linear SVM...")
                    svm_line_clf = svm_linear(train_x, train_y)
                    print("SVM Linear Linear Ready!")
                elif args[1] == "line_svm":
                    print("Fitting RBF SVM...")
                    svm_rbf_clf = svm_rbf(train_x, train_y)
                    print("SVM RBF Kernel Ready!")
                elif args[1] == "forest":
                    print("Fitting Random Forest...")
                    forest_clf = get_forest(train_x, train_y)
                    print("Random Forest Ready!")
                elif args[1] == "log":
                    print("Fitting Logistic Regression...")
                    logistic_clf = get_logistic(train_x, train_y)
                    print("Logistic Regression Ready!")
                elif args[1] == "knn":
                    print("Fitting KNN...")
                    knn_clf = get_knn(train_x, train_y)
                    print("KNN ready!")
                elif args[1] == "tree":
                    print("Fitting Decision tree...")
                    tree = get_tree(train_x, train_y)
                    print("Decision tree ready!")
                else:
                    continue
            else:
                ids_shell_args(args)
        except EOFError:
            print("CTRL-D detected, Closing now!")
            break
        except ValueError:
            print("Number Format Exception")
            continue


def ids_shell_args(args):
    try:
        # The bottom arguments will conduct both packet sniffing and pre-processing for the ids
        if args[0] == "sniff":  # args: number of packets, interface, PCAP name
            int(args[1])  # Check if it is an integer
            subprocess.run(["sudo", "tcpdump", "-c", args[1], "-s0", "-i", args[2], "-w", args[3]])
        elif args[0] == "sniff_time":
            int(args[1])    # time in seconds!
            subprocess.run(["sudo", "timeout", args[1], "tcpdump", "-i", args[2], "-s0", "-w", args[3]])
        elif args[0] == "process":  # args: pcap name
            # subprocess.run(["python3", "../Sniffer/collect.py", args[1]])
            file_parts = args[1].split('.')
            with open(file_parts[0] + ".csv", "w") as f:
                subprocess.call(["sudo", "./kdd99extractor", "-e", args[1]], stdout=f)
        elif args[0] == "process_2":  # args: pcap name
            # subprocess.run(["python3", "../Sniffer/collect.py", args[1]])
            file_parts = args[1].split('.')
            with open(file_parts[0] + ".csv", "w") as f:
                subprocess.call(["sudo", "./kdd99extractor_2", "-e", args[1]], stdout=f)
        elif args[0] == "label":  # args: pcap name
            file_parts = args[1].split('.')
            label_testing_set(args[1], "encoded_" + file_parts[0] + ".csv")

        elif args[0] == "pcap":
            file_parts = args[1].split('.')
            if len(file_parts) != 2:
                print("Not valid file name!")
                return
            if file_parts[1] != "tcpdump":
                print("Not a tcpdump file!")
                return
            subprocess.call(["tcpdump", "-r", args[1], "-w", file_parts[0] + ".pcap"])

    except ValueError:
        print("Number Format Exception!")
        return
    except IndexError:
        print("Invalid Number of arguments")
        return
    except IOError:
        print("PCAP file not found!")
        return


# THIS IS FOR LABELING TEST DATA GENERATED BY THE FUZZER!
# THE OUTPUT OF KDDPROCESSOR99 -E Spits last 5 extra columns...
# SRC IP, SRC PORT, DEST IP, DEST PORT, TIME STAMP
# SINCE U KNOW THE ATTACKS ARE BY SPECIFIC IP, USE THAT TO LABEL
# PLAY WITH COLUMN 28-32
# GOAL: LABEL IS ON FIRST COLUMN
def label_testing_set(file_path, output):
    # From fuzzer I know the mapping of IP and attack
    # 192.168.147.152 is IP of Client running Kali Linux
    attack_map = {"192.168.147.150": "back.", "192.168.147.151": "neptune.",
                  "192.168.147.152": "satan.", "192.168.147.153": "teardrop.", "192.168.147.154": "pod.",
                  "192.168.147.160": "ipsweep.", "192.168.147.161": "portsweep.", "192.168.147.162": "portsweep."}
    # Pulled from NSL-KDD Labels
    label_map = {"normal.": 11, "back.": 0, "ipsweep.": 5, "land.": 6, "neptune.": 9, "pod.": 14,
                 "portsweep.": 15, "satan.": 17, "smurf.": 18, "teardrop.": 20}

    # DON'T FORGET TO LABEL THE FEATURES. See labels.txt in NSL dataset folder
    # Protocol
    label_protocol = {
        'tcp': 1, 'udp': 2, 'icmp': 0
    }
    # Flag
    label_flag = {
        'SF': 9, 'S2': 7, 'S1': 6, 'S3': 8,
        'OTH': 0, 'REJ': 1, 'RSTO': 2, 'S0': 5, 'RSTR': 4,
        'RSTOS0': 3, 'SH': 10
    }
    # Service
    label_service = {
        'http': 24, 'smtp': 54, 'domain_u': 12, 'auth': 4,
        'finger': 18, 'telnet': 60, 'eco_i': 14, 'ftp': 19, 'ntp_u': 43,
        'ecr_i': 15, 'other': 44, 'urp_i': 65, 'private': 49, 'pop_3': 47,
        'ftp_data': 20, 'netstat': 40, 'daytime': 9, 'ssh': 56, 'echo': 13,
        'time': 63, 'name': 36, 'whois': 69, 'domain': 11, 'mtp': 35,
        'gopher': 21, 'remote_job': 51, 'rje': 52, 'ctf': 8, 'supdup': 58,
        'link': 33, 'systat': 59, 'discard': 10, 'X11': 1, 'shell': 53,
        'login': 34, 'imap4': 28, 'nntp': 42, 'uucp': 66, 'pm_dump': 45,
        'IRC': 0, 'Z39_50': 2, 'netbios_dgm': 37, 'ldap': 32, 'sunrpc': 57,
        'courier': 6, 'exec': 17, 'bgp': 5, 'csnet_ns': 7, 'http_443': 26,
        'klogin': 30, 'printer': 48, 'netbios_ssn': 39, 'pop_2': 46, 'nnsp': 41,
        'efs': 16, 'hostnames': 23, 'uucp_path': 67, 'sql_net': 55, 'vmnet': 68,
        'iso_tsap': 29, 'netbios_ns': 38, 'kshell': 31, 'urh_i': 64, 'http_2784': 25,
        'harvest': 22, 'aol': 3, 'tftp_u': 61, 'http_8001': 27, 'tim_i': 62,
        'red_i': 50, 'oth_i': 70
    }

    # Features are on Columns 1, 2, 3
    with open(file_path, "r") as read, open(output, "w+") as write:
        for line in read:
            ln = line.rstrip()
            parts = ln.split(',')

            # DON'T FORGOT TO ENCODE NOW!
            parts[1] = str(label_protocol[parts[1]])
            parts[2] = str(label_service[parts[2]])
            parts[3] = str(label_flag[parts[3]])

            # signature of land
            if parts[28] == parts[30]:
                parts.insert(0, str(label_map["land."]))
            elif parts[28] in attack_map:
                lab = attack_map[parts[28]]
                parts.insert(0, str(label_map[lab]))
            elif parts[30] in attack_map:
                lab = attack_map[parts[30]]
                parts.insert(0, str(label_map[lab]))
            else:
                parts.insert(0, str(label_map["normal."]))

            # drop the columns and write
            parts = parts[:29]
            new_line = ','.join(parts)
            write.write(new_line + '\n')
            write.flush()


def stat_column(data_set, label, column_number=2):
    freq_n = {}
    freq_a = {}
    with open(data_set, "r") as f:
        for line in f:
            try:
                # Get the right column
                row = line.split(",")
                key = row[column_number]
                if row[41] != label:
                    if key in freq_a:
                        freq_a[key] = freq_a[key] + 1
                    else:
                        freq_a[key] = 1
                else:
                    if key in freq_n:
                        freq_n[key] = freq_n[key] + 1
                    else:
                        freq_n[key] = 1

            except ValueError:
                exit("NAN FOUND!")

    # Using frequency map compute mean and std dev
    # print(mean_freq(freq_n))
    # print(std_dev_freq(freq_n))

    order_freq_n = collections.OrderedDict(sorted(freq_n.items().__iter__()))
    order_freq_a = collections.OrderedDict(sorted(freq_a.items().__iter__()))
    if len(freq_a) == 0:
        frequency_histogram(order_freq_n)
    else:
        dual_frequency_histogram(order_freq_n, order_freq_a)


# Purpose: Just get the stats. NO HISTOGRAM
def stat_one_column(data_set, label, column_number=2):
    freq_n = {}
    with open(data_set, "r") as f:
        for line in f:
            try:
                # Get the right column
                row = line.split(",")
                key = row[column_number]
                if row[0] == label:
                    if key in freq_n:
                        freq_n[key] = freq_n[key] + 1
                    else:
                        freq_n[key] = 1
                else:
                    continue
            except ValueError:
                exit("NAN FOUND!")
    # print contents
    u = mean_freq(freq_n)
    s = std_dev_freq(freq_n, u)

    # To make it easier to figure out most frequent feature value
    # sort the map by value!
    sorted_freq = OrderedDict(sorted(freq_n.items().__iter__(), key=itemgetter(1)))

    with open("stat_result_" + label + ".txt", "a+") as fd:
        fd.write("-----for Column " + str(column_number) + "-----\n")
        fd.write(print_map(sorted_freq) + '\n')
        fd.write("The mean is: " + str(u) + '\n')
        fd.write("The standard deviation is: " + str(s) + '\n')


def mean_freq(freq):
    n = sum(list(freq.values()))
    miu = 0
    for key, value in freq.items():
        miu = miu + float(key) * value
    miu = miu/n
    return miu


def print_map(hash_map, per_row=5):
    line_counter = 1
    answer = "{\n"
    for k, v in hash_map.items():
        if line_counter % per_row == 0:
            answer = answer + '\n'
        line = str(k) + ":" + str(v) + " "
        answer = answer + line
        line_counter += 1
    answer = answer + "\n}"
    return answer


def std_dev_freq(freq, miu=None):
    if miu is None:
        miu = mean_freq(freq)
    n = sum(list(freq.values()))
    sigma = 0
    for val, f in freq.items():
        sigma += f * (float(val) - miu) * (float(val) - miu)
    sigma = sigma/n
    sigma = sqrt(sigma)
    return sigma


def basic_ids():
    # Here execute commands that are needed ahead of time
    print("Running batch process of other tasks")
    if is_valid_file_type("batch.txt"):
        with open("batch.txt") as f:
            for line in f:
                ids_shell_args(line.split())
    print("Complete!")

    while True:
        try:
            # Read input from user
            arg = input("Input: ")
            args = arg.split()
            if args[0] == "exit":
                break
            else:
                ids_shell_args(args)
        except EOFError:
            print("CTRL-D detected, Closing now!")
            break
        except ValueError:
            print("Number Format Exception")
            continue


def kdd_prep_test(file):
    # I know that there are some features that need to be encoded
    # classes = LabelEncoder()
    services = LabelEncoder()
    flags = LabelEncoder()
    protocol_type = LabelEncoder()

    # Have list of stuff
    # y = ["normal.", "back.", "buffer_overflow.", "ftp_write.", "guess_passwd.",
    #             "imap.", "ipsweep.", "land.", "loadmodule.", "multihop.", "neptune.",
    #             "nmap.", "perl.", "phf.", "pod.", "portsweep.", "rootkit.", "satan.", "smurf.",
    #             "spy.", "teardrop.", "warezclient.", "warezmaster."]
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
    # classes.fit(y)
    protocol_type.fit(proto)
    flags.fit(fl)
    services.fit(serv)
    # y_hat = classes.transform(y)
    proto_hat = protocol_type.transform(proto)
    fl_hat = flags.transform(fl)
    serv_hat = services.transform(serv)

    # Build dictionary!
    # encode_class = dict(zip(y, y_hat))
    encode_protocol = dict(zip(proto, proto_hat))
    encode_fl = dict(zip(fl, fl_hat))
    encode_service = dict(zip(serv, serv_hat))
    with open("./test_labels.txt", "w") as f:
        # for k, v in encode_class.items():
        #    f.write(k + "," + str(v) + '\n')
        # f.write('\n')
        for k, v in encode_protocol.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_fl.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')
        for k, v in encode_service.items():
            f.write(k + "," + str(v) + '\n')
        f.write('\n')

    with open(file) as read_kdd_data, open("./test.csv", "w") as write_kdd:
        for line in read_kdd_data:
            # Swap using encoder
            line = line.rstrip()
            parts = line.split(",")
            # Starting from 0..
            # I must edit Column 1, 2, 3, 41
            parts[1] = str(encode_protocol[parts[1]])
            parts[2] = str(encode_service[parts[2]])
            parts[3] = str(encode_fl[parts[3]])
            # parts[41] = str(encode_class[parts[41]])
            # As my ML stuff excepts class on first column
            # swap_positions(parts, 0, 41)
            new_line = ','.join(parts)
            write_kdd.write(new_line + '\n')
            write_kdd.flush()
    print("KDD Label encoding complete!")


def load_test(test_set):
    test_x, test_y = read_data(test_set)
    forest_clf = load('random_forest.joblib')
    logistic_clf = load('logistic.joblib')
    knn_clf = load('knn.joblib')
    tree = load('tree.joblib')
    bayes_load_test(test_set, test_x, test_y)
    discriminant_load_test(test_set, test_x, test_y)
    forest_test(forest_clf, test_x, test_y)
    log_linear_test(logistic_clf, test_x, test_y)
    knn_test(knn_clf, test_x, test_y)
    tree_test(tree, test_x, test_y)


def stats_columns(label):
    for col in range(0, 29, 1):
        stat_one_column('NSL_KDD_train.csv', label, column_number=col)


if __name__ == "__main__":
    main()
