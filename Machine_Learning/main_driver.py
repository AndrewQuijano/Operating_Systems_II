#!/usr/bin/env python3

from bayes import *
from discriminant import *
from KNN import *
from logistic_regression import *
# from neural_network import *
from random_forest import *
from svm import *
from decision_tree import *
from sys import argv, exit
from convert_tcpdump import convert_tcp_dump_to_text
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
import subprocess
# import pyshark


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
    # PCAP File not accepted for training!
    if not is_valid_file_type(argv[1]):
        exit("Invalid file type! only accept.txt or .csv file extensions!")

    print("Please wait...Reading the Training Data ML...")
    train_x, train_y = read_data(argv[1])
    print("Please wait...Training Data read! Setting up ML Models!")

    print("FIT TIME FOR ONE CLASS THAT GETS TUNED")
    fit_time(train_x, train_y)
    print("Now start tuning!")

    # Now make a split between training and testing set from the input data
    start_time = time.time()
    kf = KFold(n_splits=2)

    # 1- Bayes
    print("Fitting Bayes Classifiers...")
    bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y, n_fold=kf)
    print("Bayes classifier ready!")

    # 2- LDA/QDA
    print("Fitting LDA and QDA...")
    lda_clf = discriminant_line(train_x, train_y)
    print("LDA ready!")
    # Something aboult 1 sample of class 4? Find out and maybe delete it???
    qda_clf = discriminant_quad(train_x, train_y)
    print("QDA ready!")

    # 3- SVM
    print("Fitting Linear SVM...")
    # svm_line_clf = svm_linear(train_x, train_y, n_fold=kf, slow=False)
    svm_line_clf = svm_linear_raw(train_x, train_y)

    print("SVM Linear Model Ready!")
    print("Fitting RBF SVM...")
    # svm_rbf_clf = svm_rbf(train_x, train_y, n_fold=kf, slow=False)
    svm_rbf_clf = svm_rbf_raw(train_x, train_y)
    print("SVM RBF Kernel Ready!")

    # 4- Random Forest
    print("Fitting Random Forest...")
    # forest_clf = get_forest(train_x, train_y, n_fold=kf, slow=False)
    forest_clf = get_forest_raw(train_x, train_y)
    print("Random Forest Ready!")

    # 5- Logistic Regression
    print("Fitting Logistic Regression...")
    # logistic_clf = logistic_linear(train_x, train_y, n_fold=kf, slow=False)
    logistic_clf = logistic_raw(train_x, train_y)
    print("Logistic Regression Ready!")

    # 6- KNN
    print("Fitting KNN...")
    knn_clf = raw_knn(train_x, train_y)
    # knn_clf = tune_knn(train_x, train_y, n_fold=5, slow=False)
    print("KNN ready!")

    # 7- Decision Tree
    print("Fitting Decision tree...")
    # tree = get_tree(train_x, train_y, n_fold=5, slow=False)\
    tree = decision_tree_raw(train_x, train_y)
    print("Decision tree ready!")

    print("--- Model Training Time: %s seconds ---" % (time.time() - start_time))
    print("All models are trained...")

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
            # This argument is run the IDS with the test data
            elif args[0] == "detect":  # args: csv type
                # Check if the correct CSV file exists, if so read it in!
                if not is_valid_file_type(args[1]):
                    continue
                test_x, test_y = read_data(args[1])

                # Now test it and get results. Training is done, just get Test Score, Classification Report, etc.
                svm_test(svm_line_clf, test_x, test_y, "Linear")
                svm_test(svm_rbf_clf, test_x, test_y, "Radial")
                forest_test(forest_clf, test_x, test_y)
                log_linear_test(logistic_clf, test_x, test_y)
                knn_test(knn_clf, train_x, train_y)
                lda_test(lda_clf, test_x, test_y)
                qda_test(qda_clf, test_x, test_y)
                tree_test(tree, test_x, test_y)
                naive_bayes_test(bayes, bayes_isotonic, bayes_sigmoid, test_x, test_y)
            else:
                ids_shell_args(args)
        except KeyboardInterrupt:
            print("CTRL-C detected, Closing now!")
            break
        except EOFError:
            print("CTRL-D detected, Closing now!")
            break


def ids_shell_args(args):
    try:
        # The bottom arguments will conduct both packet sniffing and pre-processing for the ids
        if args[0] == "sniff":  # args: number of packets, interface, PCAP name
            int(args[1])  # Check if it is an integer
            subprocess.run(["sudo", "tcpdump", "-c", args[1], "-s0", "-i", args[2], "-w", args[3]])
        elif args[0] == "process":  # args: pcap name
            subprocess.run(["python3", "../Sniffer/collect.py", args[1]])

        # DO NOT USE THIS! THIS ASSUMES TEXT TO PCAP
        # YOU DONT NEED THIS IF YOU HAVE TCPDUMP
        elif args[0] == "convert":  # args: file.tcpdump
            file_parts = args[1].split('.')
            if len(file_parts) != 2:
                print("Not valid file name!")
                print(file_parts[0])
                print(file_parts[1])
                return
            if file_parts[1] != "tcpdump":
                print("Not a tcpdump file!")
                return
            # Step 1- Convert tcpdump to textfile that can be read!
            with open(file_parts[0] + ".txt", "w") as f:
                subprocess.call(["tcpdump", "-r", file_parts[0] + ".tcpdump"], stdout=f)
            print(file_parts[1] + ".txt is generated!")

            # Step 2- convert the readable tcpdump to the right format
            convert_tcp_dump_to_text(file_parts[0] + ".txt", file_parts[0] + "2.txt")
            print(file_parts[1] + "2.txt is generated")

            # Step 3- complete conversion to PCAP format
            subprocess.run(["text2pcap", file_parts[0] + "2.txt", file_parts[0] + ".pcap"])
            print("Conversion Complete!")

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
    except IOError:
        print("PCAP file not found!")
        return


# Label the PCAP using ID in PCAP
# Labels is a Hashmap<int, string> where int is the packet id in Wireshark, String is attack name
def label_training_set(labels, pcap_file, no_label_benign=False):
    # labels is a dictionary of packet ID
    # {1:"syn_flood", 2:"neptune",5:"syn_flood"}
    le = LabelEncoder()
    attacks = set(labels.values())
    if no_label_benign:
        attacks.add("Benign")
    le.fit(attacks)
    y = []
    capture = pyshark.FileCapture(pcap_file)
    for packet_id in range(len(capture)):
        if labels[packet_id] is not None:
            y.append(labels[packet_id])
        else:
            y.append("Benign")

    # Convert the List of classes to NP Array
    # Then, turn to column vector!
    np_y = np.asarray(le.transform(y))
    np.transpose(np_y)


# dummy test, build label for training data
# def label_training_set(pcap_file):
#    capture = pyshark.FileCapture(pcap_file)
#    for packet in capture:
#        try:
#            print(packet)
#        except AttributeError:
#            continue


def stat_column(data_set, label, column_number=2, check_label=False):
    freq = {}
    with open(data_set, "r") as f:
        for line in f:
            try:
                # Get the right column
                row = line.split(",")
                if row[0] != label and check_label:
                    continue
                key = row[column_number]
                if key in freq:
                    freq[key] = freq[key] + 1
                else:
                    freq[key] = 1
            except ValueError:
                exit("NAN FOUND!")

    # Using frequency map compute mean and std dev
    n = sum(list(freq.values()))
    miu = 0
    for key, value in freq.items():
        miu = miu + float(key) * value
    miu = miu / n

    # compe sigma
    sigma = 0
    for key, value in freq.items():
        sigma = sigma + value * (float(key) - miu) * (float(key) - miu)
    sigma = sigma / (n - 1)
    # Print it and plot a histogram to view distribution...


# This was created because lack of time
# I need to know how long it takes to fit each classifier.
# Then I can just use some basic math to figure out how much CV I can do
def fit_time(train_x, train_y):
    raw_knn(train_x, train_y)
    logistic_raw(train_x, train_y)
    decision_tree_raw(train_x, train_y)
    get_forest_raw(train_x, train_y)
    svm_linear_raw(train_x, train_y)
    svm_rbf_raw(train_x, train_y)


if __name__ == "__main__":
    ids()
