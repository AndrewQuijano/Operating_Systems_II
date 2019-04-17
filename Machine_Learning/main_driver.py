#!/usr/bin/env python3

from bayes import *
from discriminant import *
from KNN import *
from logistic_regression import *
from neural_network import *
from random_forest import *
from svm import *
from decision_tree import *
from sys import argv, exit
from convert_tcpdump import convert_tcpdump_to_text2pcap
import subprocess


def read_data(file, skip_head=True):
    if skip_head:
        features = np.genfromtxt(file, delimiter=',', skip_header=1, dtype=float, autostrip=True, converters=None)
    else:
        features = np.genfromtxt(file, delimiter=',', skip_header=0, dtype=float, autostrip=True, converters=None)

    if np.isnan(features).any():
        if skip_head:
            features = np.genfromtxt(file, delimiter=',', skip_header=1, dtype=str, autostrip=True, converters=None)
        else:
            features = np.genfromtxt(file, delimiter=',', skip_header=0, dtype=str, autostrip=True, converters=None)
        classes = features[:, 0]
        features = features[:, 1:]
        # Now you have NaN in your features, ok now you have issues!
        if np.isnan(features).any():
            print("There are NaNs found in your features at: " + str(list(map(tuple, np.where(np.isnan(features))))))
            exit(0)
        else:
            features.astype(float)
    else:
        classes = features[:, 0]
        features = features[:, 1:]

    return features, classes


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

    # Now train ALL classifiers!

    # 1- SVM
    start_time = time.time()
    svm_line_clf = svm_linear(train_x, train_y)
    svm_rbf_clf = svm_rbf(train_x, train_y)
    svm_test(svm_line_clf, test_x, test_y, "Linear")
    svm_test(svm_rbf_clf, test_x, test_y, "Radial")

    # 2- Random Forest
    forest_clf = get_forest(train_x, train_y)
    forest_test(forest_clf, test_x, test_y)

    # 3- Neural Networks
    # brain_clf = get_brain(train_x, train_y)
    # brain_test(brain_clf, test_x, test_y)

    # 4- Logistic Regression
    logit_clf = logistic_linear(train_x, train_y)
    log_linear_test(logit_clf, test_x, test_y)

    # 5- KNN
    knn_clf = tune_knn(train_x, train_y)
    knn_test(knn_clf, train_x, train_y)

    # 6- LDA/QDA
    lda_clf = discriminant_line(train_x, train_y)
    qda_clf = discriminant_quad(train_x, train_y)
    lda_test(lda_clf, test_x, test_y)
    qda_test(qda_clf, test_x, test_y)

    # 7- Bayes
    bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y)
    naive_bayes_test(bayes, bayes_isotonic, bayes_sigmoid, test_x, test_y)

    # 8- Decision Tree
    tree = get_tree(train_x, train_y)
    tree_test(tree, test_x, test_y)
    print("---Time to complete training everything: %s seconds---" % (time.time() - start_time))


# Use this to run IDS using Classifier!
def ids():
    # To run the program I need either
    # 1- the raw PCAP with labels?
    # 2- just the raw CSV pre-processed using Stolfo's KDD Data mining techniques

    if len(argv) != 2:
        exit("usage: python3 main_ids <training data set>")

    if not is_valid_file_type(argv[1]):
        exit("Invalid file type! only accept.txt or .csv file extensions!")

    print("Please wait...Training all ML models...")
    # With the training file ready, get all models trained!
    train_x, train_y = read_data(argv[1])
    # Now make a split between training and testing set from the input data

    # 1- SVM
    svm_line_clf = svm_linear(train_x, train_y)
    # svm_rbf_clf = svm_rbf(train_x, train_y)

    # 2- Random Forest
    # forest_clf = get_forest(train_x, train_y)

    # 3- Logistic Regression
    # logistic_clf = logistic_linear(train_x, train_y)

    # 4- KNN
    # knn_clf = tune_knn(train_x, train_y)

    # 5- LDA/QDA
    # lda_clf = discriminant_line(train_x, train_y)
    # qda_clf = discriminant_quad(train_x, train_y)

    # 6- Bayes
    # bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y)

    # 7- Decision Tree
    # tree = get_tree(train_x, train_y)

    print("All models are trained...")

    # Here execute commands that are needed ahead of time
    print("Running batch process of other tasks")
    if is_valid_file_type("./batch.txt"):
        with open("./batch.txt") as file:
            for line in file:
                print(line)
    print("Complete!")

    while True:

        try:
            # Read input from user
            args = input("Input: ")
            # args = argv.split()
            if args == "exit":
                break
            # This argument is run the IDS with the test data
            elif args == "detect":  # args: csv type
                # Check if the correct CSV file exists, if so read it in!
                if not is_valid_file_type("./record.csv"):
                    return

                test_x, test_y = read_data("./record.csv")

                # Now test it and get results. Training is done, just get Test Score, Classification Report, etc.
                svm_test(svm_line_clf, test_x, test_y, "Linear")
                # svm_test(svm_rbf_clf, test_x, test_y, "Radial")
                # forest_test(forest_clf, test_x, test_y)
                # log_linear_test(logistic_clf, test_x, test_y)
                # knn_test(knn_clf, train_x, train_y)
                # lda_test(lda_clf, test_x, test_y)
                # qda_test(qda_clf, test_x, test_y)
                # tree_test(tree, test_x, test_y)
                # naive_bayes_test(bayes, bayes_isotonic, bayes_sigmoid, test_x, test_y)
            else:
                ids_shell_args(args)
        except KeyboardInterrupt:
            print("CTRL-C detected, Closing now!")
            break
        except EOFError:
            print("CTRL-D detected, Closing now!")
            break


def ids_shell_args(args):
    # The bottom arguments will conduct both packet sniffing and pre-processing for the ids
    if args == "sniff":  # args: number of packets, interface, PCAP name
        subprocess.run(["sudo", "tcpdump", "-c", "500", "-s0", "-i", "ens33", "-w", "sniff.pcap"])
    elif args == "process":  # args: pcap name
        subprocess.run(["python3", "../Sniffer/collect.py", "sniff.pcap"])

    # These three must be executed in order to convert a normal tcpdump to .pcap automatically in order
    elif args == "tcpdump2txt":  # args: file.tcpdump file.txt
        subprocess.run(["tcpdump", "-r", "outside.tcpdump", "outside.txt"])
    elif args == "fix":  # args: file.txt file_hex.txt
        convert_tcpdump_to_text2pcap("../../outside.txt", "outside.txt")
    elif args == "convert":  # args: convert .txt .pcap
        subprocess.run(["text2pcap", "-l", "101", "outside.txt", "outside.pcap"])


# dummy test, build label for training data
def label_training_set(pcap_file):
    import pyshark
    capture = pyshark.FileCapture(pcap_file)
    for packet in capture:
        try:
            print(packet)
        except AttributeError:
            continue


# dummy test, build label
def label_test_set(source_ip, destination_ip, pcap_file):
    import pyshark
    capture = pyshark.FileCapture(pcap_file)
    for packet in capture:
        try:
            print(packet)
        except AttributeError:
            continue


if __name__ == "__main__":
    main()
