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


def read_data(file, skip_head=False):
    if skip_head:
        features = np.genfromtxt(file, delimiter=',', skip_header=1, dtype=float, autostrip=True, converters=None)
    else:
        features = np.genfromtxt(file, delimiter=',', skip_header=0, dtype=float, autostrip=True, converters=None)
    classes = features[:, 0].copy()
    features = features[:, 1:]
    if np.isnan(features).any():
        print("NaN found in X!")
        print(np.argwhere(np.isnan(features)))
    if np.isnan(classes).any():
        print("NaN found in Y!")
        np.argwhere(np.isnan(classes))
    return features, classes


def main():

    # Check if both sets are available
    if len(argv) != 3:
        print("Usage: python3 main_driver <train-set> <test-set>")
        exit(0)

    # Read the training and testing data-set
    # This assumes the class variable is on the first column!
    # It also assumes all data is numeric!
    train_x, train_y = read_data(argv[1])
    test_x, test_y = read_data(argv[2])
    print(train_x)
    print("Space")
    print(train_y)

    # Now train ALL classifiers!
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


if __name__ == "__main__":
    main()
