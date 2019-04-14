# first of all import the socket library
# main issue: http://scikit-learn.org/stable/modules/scaling_strategies.html
from network_setup import *
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron, SGDClassifier, SGDRegressor
from sklearn.linear_model import PassiveAggressiveRegressor, PassiveAggressiveClassifier
import numpy as np

# ORIGINAL PARTS WHICH ALREADY ARE INCREMENTAL!


# Return X, Y for training, or just X to be used for classifiers
def parse_string_to_numpy(data, training_phase=True):
    #try:

    #if training_phase:
    x = np.fromstring(data, dtype='float32', sep=',')
    y = x[0]
    x = x[1:]
    x = x.reshape(1, -1)
    y = y.reshape(1, -1)
    return x, y
    #else:
    #   x = np.fromstring(args, dtype=float, sep=',')
    #   return x, None
    #except ValueError:
    #    return None, None


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

                bayes.partial_fit(x, y, classes=None)
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
def main():
    # Once server socket is ready get all classifiers up!
    bayes = MultinomialNB(class_prior=None, fit_prior=True)
    percep = Perceptron()
    sgd_class = SGDClassifier()
    pa_classifier = PassiveAggressiveClassifier()
    sgd_regress = SGDRegressor()
    pa_regress = PassiveAggressiveRegressor()

    # For Partial fit to work, I need to know all classes ahead of time!
    classes = [3.0, 5.0, 6.0, 8.0]

    # Train it
    with open("zip_train.csv", "r") as file:
        for line in file:
            print(line)
            x, y = parse_string_to_numpy(line.rstrip())
            print("NUMPY")
            print(x)
            print(y)
            # bayes.partial_fit(x, y, classes=classes)
            # WORKS
            # percep.partial_fit(x, y, classes=classes)
            sgd_class.partial_fit(x, y, classes=classes)
            pa_classifier.partial_fit(x, y, classes=classes)
            #sgd_regress.partial_fit(x, y, classes=classes)
            #pa_regress.partial_fit(x, y, classes=classes)

    # Now test it!


if __name__ == "__main__":
    main()
