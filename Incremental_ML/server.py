#!/usr/bin/env python3

# first of all import the socket library
# main issue: http://scikit-learn.org/stable/modules/scaling_strategies.html
from network_setup import *
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.linear_model import Perceptron, SGDClassifier, SGDRegressor
# from sklearn.linear_model import PassiveAggressiveRegressor, PassiveAggressiveClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, classification_report
from misc import make_confusion_matrix, read_data, is_valid_file_type, label_testing_set
from tuning import *
import numpy as np
from joblib import dump, load
from sys import argv


# ORIGINAL PARTS WHICH ALREADY ARE INCREMENTAL!
def init_classifiers(train_x, train_y):
    if train_x is None or train_y is None:
        bayes = MultinomialNB()
        percep = Perceptron(warm_start=True, max_iter=10, tol=1e-3)
        sgd_class = SGDClassifier(warm_start=True, max_iter=10, tol=1e-3)
        pa_classifier = PassiveAggressiveClassifier(warm_start=True, max_iter=10, tol=1e-3)
        sgd_regress = SGDRegressor(warm_start=True, max_iter=10, tol=1e-3)
        pa_regress = PassiveAggressiveRegressor(warm_start=True, max_iter=10, tol=1e-3)
    else:
        kf = KFold(n_splits=10)
        bayes = tune_bayes(train_x, train_y, kf, False)
        percep = tune_perceptron(train_x, train_y, kf, False)
        sgd_class = tune_sgd_clf(train_x, train_y, kf, False)
        sgd_regress = tune_passive_aggressive_reg(train_x, train_y, kf, False)
        pa_classifier = tune_passive_aggressive_clf(train_x, train_y, kf, False)
        pa_regress = tune_passive_aggressive_reg(train_x, train_y, kf, False)
        # Get Parameters now
        with open("results.txt", "w+") as fd:
            fd.write("[bayes] Best Parameters: " + str(bayes.best_params_) + '\n')
            fd.write("[percep] Best Parameters: " + str(percep.best_params_) + '\n')
            fd.write("[sgd_class] Best Parameters: " + str(sgd_class.best_params_) + '\n')
            fd.write("[pa_classifier] Best Parameters: " + str(pa_classifier.best_params_) + '\n')
            fd.write("[sgd_regress] Best Parameters: " + str(sgd_regress.best_params_) + '\n')
            fd.write("[pa_regress] Best Parameters: " + str(pa_regress.best_params_) + '\n')

            fd.write("[bayes] Training Score: " + str(bayes.score(train_x, train_y)) + '\n')
            fd.write("[percep] Training Score: " + str(percep.score(train_x, train_y)) + '\n')
            fd.write("[sgd_class] Training Score: " + str(sgd_class.score(train_x, train_y)) + '\n')
            fd.write("[pa_classifier] Training Score: " + str(pa_classifier.score(train_x, train_y)) + '\n')
            fd.write("[sgd_regress] Training Score: " + str(sgd_regress.score(train_x, train_y)) + '\n')
            fd.write("[pa_regress] Training Score: " + str(pa_regress.score(train_x, train_y)) + '\n')
        # If trained, should just dump now...
        dump(bayes, "i_bayes.joblib")
        dump(sgd_class, "sgd_class.joblib")
        dump(sgd_regress, "sgd_regress.joblib")
        dump(pa_classifier, "PA_class.joblib")
        dump(pa_regress, "PA_regress.joblib")
        dump(percep, "percep.joblib")
    return [bayes, percep, sgd_class, pa_classifier, sgd_regress, pa_regress]


# Return X, Y for training, or just X to be used for classifiers
# This will ONLY WORK FOR ONE LINE!
def parse_string_to_numpy(data, training_phase=True):
    try:
        if training_phase:
            x = np.fromstring(data, dtype='float32', sep=',')
            y = x[0]
            x = x[1:]
            x = x.reshape(1, -1)
            y = y.reshape(1, -1)
            return x, y
        else:
            x = np.fromstring(data, dtype='float32', sep=',')
            x = x[1:]
            x = x.reshape(1, -1)
            return x, None
    except ValueError:
        return None, None


def server():
    server_socket = create_server_socket(12345)
    if server_socket is None:
        die("Failed to make Server Socket!")

    # Once server socket is ready get all classifiers up!
    bayes = MultinomialNB(class_prior=None, fit_prior=True)
    perceptron = Perceptron()
    sgd_class = SGDClassifier()
    pa_classifier = PassiveAggressiveClassifier()
    sgd_regressor = SGDRegressor()
    pa_regressor = PassiveAggressiveRegressor()

    # For Partial fit to work, I need to know all classes ahead of time!
    while True:
        try:

            # Establish connection with client.
            connection, address = server_socket.accept()
            print('Got connection from: ', address)

            # When starting to run server you have the following options
            # 1- Train model
            # Write to .csv file for tuning, update all models
            # 2- Test Model
            # input the features, get results and send back to client
            # 3- exit

            # input example, first column is the command, second column is label
            # To keep things simple, assume a comma separated string!
            # "train", 1, 0.25, 0.6, 0.8
            # "test", 0.5, 20, 2,
            # "exit"

            # ---PLEASE NOTE CURRENTLY THIS IS BUILD WITH ONE THING AT A TIME!---
            data = connection.recv(1024).decode()
            print("Input is: " + data)
            args = data.split(",")

            if args[0] == "train":
                x, y = parse_string_to_numpy(data, True)
                # Error occurred in converting string to numpy!
                if x is None:
                    connection.close()
                    continue

                # 1- Write the data to a CSV file
                with open("data_set.csv") as file:
                    file.write(data + '\n')

                # 2- Check if it is time to tune classifier?

                # 3- Update Classifiers

                bayes.partial_fit(x, y)
                connection.close()

            elif args[0] == "test":
                x, y = parse_string_to_numpy(data, False)
                # Error occurred in converting string to numpy!
                if x is None:
                    connection.close()
                    continue
                # Run the prediction and send the results back!
                else:
                    y_pred = bayes.predict(x)
                    connection.send(np.array_str(np.arange(1)).encode())
                connection.close()

            elif args[0] == "exit":
                connection.close()
                break

            else:
                connection.close()
                continue

        except KeyboardInterrupt:
            print('CTRL-C received, Exit!')
            break

    server_socket.close()


# test driver only on local host with ML model, see main_driver in ML python library
# Test with ZIP code data set
def main(train_data):
    # Once server socket is ready get all classifiers up!
    # For Partial fit to work, I need to know all classes ahead of time!
    # classes = [3.0, 5.0, 6.0, 8.0]

    train_x, train_y = read_data(train_data)
    class_names = ["bayes", "percep", "sgd_class", "pa_classifier", "sgd_regress", "pa_regress"]
    # classes = np.arange(0, 23, 1, dtype=float)
    # [0, 23) or [0, 22]
    classifiers = init_classifiers(train_x, train_y)

    # Train it
    # TODO: Read say 100 lines, make to Numpy THEN FIT
    # with open(train_data, "r") as file:
    #    for line in file:
    #        x, y = parse_string_to_numpy(line.rstrip())
    #        for clf in classifiers:
    #            clf.partial_fit(x, y, classes=classes)

    # Ideally figure out how to tune after partial fit ONCE in...
    # I guess would I technically keep a record and try to refit?

    while True:
        try:
            arg = input("Input: ")
            args = arg.split()
            if args[0] == "exit":
                break

            elif args[0] == "detect":  # args: csv type
                # Check if the correct CSV file exists, if so read it in!
                if not is_valid_file_type(args[1]):
                    continue
                test_x, test_y = read_data(args[1])
                for idx in range(len(classifiers)):
                    incremental_test(classifiers[idx], test_x, test_y, class_names[idx])
        except KeyboardInterrupt:
            break
        except EOFError:
            break


def incremental_test(clf, test_x, test_y, clf_name):
    y_hat = clf.predict(test_x)

    print("Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))
    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=clf, clf_name=clf_name)

    with open("results.txt", "a") as my_file:
        my_file.write("[" + clf_name + "] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[" + clf_name + "]---\n")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat, labels=clf.classes_,
                                            target_names=[str(i) for i in clf.classes_]))
        my_file.write('\n')


def load_test(file_path):
    test_x, test_y = read_data(file_path)
    bayes = load("i_bayes.joblib")
    sgd = load("sgd_class.joblib")
    pa = load("PA_class.joblib")
    percep = load("percep.joblib")
    incremental_test(bayes, test_x, test_y, "Bayes")
    incremental_test(sgd, test_x, test_y, "SGD")
    incremental_test(pa, test_x, test_y, "Passive_Aggressive")
    incremental_test(percep, test_x, test_y, "Perceptron")


if __name__ == "__main__":
    load_test("./shit.csv")
    # if len(argv) == 1:
    #    main("./NSL_KDD_train.csv")
    # else:
    #    main(argv[1])
