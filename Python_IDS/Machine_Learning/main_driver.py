from bayes import *
from discriminant import *
from KNN import *
from logistic_regression import *
from neural_network import *
from random_forest import *
from svm import *
from decision_tree import *
from sys import argv, exit

def read_data(file):
    features = np.genfromtxt(file, delimiter=',', skip_header=0, dtype=float, autostrip=True, converters=None)
    classes = features[:, 1].copy()
    features = features[:, 1:]
    return features, classes

def main():

    # Check if both sets are available
    if len(arv) != 2:
        print("Usage: python3 main_driver <train-set> <test-set>")

    # Read the training and testing data-set
    # This assumes the class variable is on the first column!
    # It also assumes all data is numeric!
    train_x, train_y = read_data(argv[0])
    test_x, test_y = get_cv_set(args[1])
    print(train_x)
    print(train_y)

    # Now train ALL classifiers!
    # 1- SVM
    #svm_line_clf = svm_linear(train_x, train_y, test_x, test_y)
    #svm_rbf_clf = svm_rbf(train_x, train_y, test_x, test_y)

    # 2- Random Forest
    #forest_clf = get_forest(train_x, train_y, test_x, test_y)

    # 3- Neural Networks
    #brain_clf = get_brain(train_x, train_y, test_x, test_y)

    # 4- Logistic Regression
    #logit_clf = logistic_linear(train_x, train_y, test_x, test_y)

    # 5- KNN
    #knn_clf = tune_knn(train_x, train_y, test_x, test_y)

    # 6- LDA/QDA
    #lda_clf = discriminant_line(train_x, train_y, test_x, test_y)
    #qda_clf = discriminant_quad(train_x, train_y, test_x, test_y)

    # 7- Bayes
    #bayes, bayes_istonic, bayes_sigmoid = naive_bayes(train_x, train_y, test_x, test_y)

    # 8- Decision Tree
    #tree = get_tree(train_x, train_y, test_x, test_y)


if __name__ == "__main__":
    main()
