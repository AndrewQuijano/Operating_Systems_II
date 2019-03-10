# first of all import the socket library
# main issue: http://scikit-learn.org/stable/modules/scaling_strategies.html
from network_setup import *
from sklearn.naive_bayes import MultinomialNB

# ORIGINAL PARTS WHICH ALREADY ARE INCREMENTAL!
#from random_forest import tune_forest
#from logistic_regression import *
#from neural_network import *


# Return X, Y for training, or just X to be used for classifiers
def parse_data(data, training_phase=True):
    if training_phase:
        return data
    else:
        return data


def main():
    server_socket = create_server_socket(12345)
    if server_socket is None:
        die("Failed to make Server Socket!")

    # Once server socket is ready get all classifiers up!
    bayes = MultinomialNB(class_prior=None, fit_prior=True)

    while True:
        try:
            # Establish connection with client.
            connection, address = server_socket.accept()
            print('Got connection from: ', address)

            # 1- Get (x, y)
            # 1- Get the data from the client
            x = connection.recv(4).decode()
            y = connection.recv(4).decode()
            print("Input is: " + str(x) + "," + str(y))

            # 2- fit again with all classifier
            bayes.partial_fit(x, y)

            connection.close()

        except KeyboardInterrupt:
            print('CTRL-C received, Exit!')
            break

    # Perhaps I can do a while loop to have only training?
    while True:
        try:
            # Establish connection with client.
            connection, address = server_socket.accept()
            print('Got connection from: ', address)

            # 1- Get the data from the client
            x = connection.recv(4).decode()

            # 2- Test with Classifier
            bayes.partial_fit(x, y)

            # Allow for option to resume training?

            connection.close()

        except KeyboardInterrupt:
            print('CTRL-C received, Exit!')
            break
    server_socket.close()


if __name__ == "__main__":
    main()