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
    svm_line_clf = svm_linear(train_x, train_y, test_x, test_y)
    svm_rbf_clf = svm_rbf(train_x, train_y, test_x, test_y)
    svm_test(svm_line_clf, test_x, test_y, "Linear")
    svm_test(svm_rbf_clf, test_x, test_y, "Radial")

    # 2- Random Forest
    forest_clf = get_forest(train_x, train_y, test_x, test_y)
    forest_test(forest_clf, test_x, test_y)

    # 3- Neural Networks
    brain_clf = get_brain(train_x, train_y, test_x, test_y)
    brain_test(brain_clf, test_x, test_y)

    # 4- Logistic Regression
    logit_clf = logistic_linear(train_x, train_y, test_x, test_y)
    log_linear_test(logit_clf, test_x, test_y)

    # 5- KNN
    knn_clf = tune_knn(train_x, train_y, test_x, test_y)
    knn_test(knn_clf, train_x, train_y)

    # 6- LDA/QDA
    lda_clf = discriminant_line(train_x, train_y, test_x, test_y)
    qda_clf = discriminant_quad(train_x, train_y, test_x, test_y)
    lda_test(lda_clf, test_x, test_y)
    qda_test(qda_clf, test_x, test_y)

    # 7- Bayes
    bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y)
    naive_bayes_test(bayes, bayes_isotonic, bayes_sigmoid, test_x, test_y)

    # 8- Decision Tree
    tree = get_tree(train_x, train_y, test_x, test_y)
    tree_test(tree, test_x, test_y)


# Use this to run IDS using Classifier!
def ids():
    import subprocess
    # To run the program I need either
    # 1- the raw PCAP with labels?
    # 2- just the raw CSV pre-processed using Stolfo's KDD Data mining techniques

    if len(argv) == 2:
        print("usage: python3 main_ids <training data set>")

    if not is_valid_file_type(argv[1]):
        exit("Invalid file type! only accept.txt or .csv file extensions!")

    # With the training file ready, get all models trained!
    train_x, train_y = read_data(argv[1])
    # Now make a split between training and testing set from the input data

    # 1- SVM
    svm_line_clf = svm_linear(train_x, train_y)
    svm_rbf_clf = svm_rbf(train_x, train_y)

    # 2- Random Forest
    forest_clf = get_forest(train_x, train_y)

    # 3- Logistic Regression
    logistic_clf = logistic_linear(train_x, train_y)

    # 4- KNN
    knn_clf = tune_knn(train_x, train_y)

    # 5- LDA/QDA
    lda_clf = discriminant_line(train_x, train_y)
    qda_clf = discriminant_quad(train_x, train_y)

    # 6- Bayes
    bayes, bayes_isotonic, bayes_sigmoid = naive_bayes(train_x, train_y)

    # 7- Decision Tree
    tree = get_tree(train_x, train_y)

    # run python3 collect.py <.pcap>
    while True:

        try:
            file = input("Input test PCAP file:")
            subprocess.run(["python3", file])

            # Force to wait until ready to analyze
            # When done, read the test data generated from the packet sniffer

            # Check if the correct CSV file exists, if so read it in!
            if not is_valid_file_type("./record.csv"):
                continue

            test_x, test_y = read_data("./record.csv")

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

        except KeyboardInterrupt:
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
