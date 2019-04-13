#!/usr/env/python3
from sys import argv
from Attacker import isvalid
from MachineLearing import *
import subprocess


def main():
    # To run the program I need either
    # 1- the raw PCAP with labels?
    # 2- just the raw CSV pre-processed using Stolfo's KDD Data mining techniques
    if len(argv) == 2:
        print("usage: python3 main_ids <training data set>")

    if not valid_extension(argv[1], "csv"):
        exit("Invalid file type!")

    # With the training file ready, get all models trained!

    train_x, train_y = read_data(argv[1])
    # Now make a split between training and testing set from the input data
    train_x, train_y, test_x, test_y = get_cv_set(train_x, train_y)

    # 1- SVM
    svm_line_clf = svm_linear(train_x, train_y, test_x, test_y)
    svm_rbf_clf = svm_rbf(train_x, train_y, test_x, test_y)

    # 2- Random Forest
    forest_clf = get_forest(train_x, train_y, test_x, test_y)

    # 3- Neural Networks
    brain_clf = get_brain(train_x, train_y, test_x, test_y)

    # 4- Logistic Regression
    logit_clf = logistic_linear(train_x, train_y, test_x, test_y)

    # 5- KNN
    knn_clf = tune_knn(train_x, train_y, test_x, test_y)

    # 6- LDA/QDA
    lda_clf = discriminant_line(train_x, train_y, test_x, test_y)
    qda_clf = discriminant_quad(train_x, train_y, test_x, test_y)

    # 7- Bayes
    bayes, bayes_istonic, bayes_sigmoid = naive_bayes(train_x, train_y, test_x, test_y)

    # 8- Decision Tree
    tree = get_tree(train_x, train_y, test_x, test_y)

    # run python3 collect.py <.pcap>
    while True:

        try:
            file = input("Input test PCAP file:")
            subprocess.run(["python3", file])

            # Force to wait until ready to analyze
            # When done, read the test data generated from the packet sniffer

            # Check if the correct CSV file exists, if so read it in!
            test_x, test_y = read_data("./record.csv")

            # Now test it and get results. Training is done, just get Test Score, Classification Report, etc.
            naive_bayes_test(bayes, bayes_istonic, bayes_sigmoid, test_x, test_y)

        except KeyboardInterrupt:
            break
        except EOFError:
            break


if __name__ == "main":
    main()
