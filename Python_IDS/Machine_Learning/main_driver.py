from bayes import *
from discriminant import *
from KNN import *
from logistic_regression import *
from neural_network import *
from random_forest import *
from svm import *
from decision_tree import *


# Using ZIP code data set to test strength of all scripts...
def read_zip_data_set():
    # Read the data set...
    train_3 = "./train_3.txt"
    train_5 = "./train_5.txt"
    train_6 = "./train_6.txt"
    train_8 = "./train_8.txt"

    # convert = {1: lambda x: x.decode('utf_8')}
    train_3_x = np.genfromtxt(train_3, delimiter=',', skip_header=0, dtype=float, autostrip=True, converters=None)
    train_5_x = np.genfromtxt(train_5, delimiter=',', skip_header=0, dtype=float, autostrip=False, converters=None)
    train_6_x = np.genfromtxt(train_6, delimiter=',', skip_header=0, dtype=float, autostrip=False, converters=None)
    train_8_x = np.genfromtxt(train_8, delimiter=',', skip_header=0, dtype=float, autostrip=False, converters=None)

    # Delete first column, which had a blank...
    # print(np.shape(train_3_x))
    # train_3_x = np.delete(train_3_x, [1], axis=1)
    # print(train_3_x)

    # SAME AS ROW BIND in R
    x = np.vstack((train_3_x, train_5_x, train_6_x, train_8_x))

    train_3_y = np.zeros(train_3_x.shape[0])
    train_3_y = train_3_y + 3

    train_5_y = np.zeros(train_5_x.shape[0])
    train_5_y = train_5_y + 5

    train_6_y = np.zeros(train_6_x.shape[0])
    train_6_y = train_6_y + 6

    train_8_y = np.zeros(train_8_x.shape[0])
    train_8_y = train_8_y + 8

    # Build the column of Y
    y = np.append(train_3_y, train_5_y)
    y = np.append(y, train_6_y)

    y = np.append(y, train_8_y)
    y = np.transpose(y)
    return x, y


def main():
    # Read the Data...
    train_x, train_y = read_zip_data_set()
    train_x, train_y, test_x, test_y = get_cv_set(train_x, train_y)
    print("Got the Data Set!")

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
