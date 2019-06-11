from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from misc import *
import time
from joblib import dump, load


def discriminant_line(train_x, train_y):
    lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
    start_time = time.time()
    lda.fit(train_x, train_y)
    print("--- Time to fit LDA: %s seconds ---" % (time.time() - start_time))
    print("Training Score (LDA): " + str(lda.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[LDA] Training Mean Test Score: " + str(lda.score(train_x, train_y)) + '\n')
    dump(lda, "./Classifiers/LDA.joblib")
    return lda


def lda_test(clf, test_x, test_y, extra_test=False):
    num_test_y = len(np.unique(test_y))
    y_hat = clf.predict(test_x)
    print("Testing Score is (LDA): " + str(accuracy_score(test_y, y_hat)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[LDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    if num_test_y == len(clf.classes_):
        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[LDA]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                                labels=[str(i) for i in clf.classes_],
                                                target_names=[str(i) for i in clf.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_predict=y_hat, clf=clf, clf_name='LDA')
    else:
        print("Not full test set!")

    if extra_test:
        top(lda, test_x, test_y, "LDA", extra_attempts=1)
        top(lda, test_x, test_y, "LDA", extra_attempts=3)


def discriminant_quad(train_x, train_y):
    qda = QuadraticDiscriminantAnalysis(store_covariance=False)
    start_time = time.time()
    qda.fit(train_x, train_y)
    print("--- Time to fit QDA: %s seconds ---" % (time.time() - start_time))
    print("Training Score is (QDA): " + str(qda.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[QDA] Training Mean Test Score: " + str(qda.score(train_x, train_y)) + '\n')
    dump(qda, "./Classifiers/QDA.joblib")
    return qda


def qda_test(clf, test_x, test_y, extra_test=False):
    num_test_y = len(np.unique(test_y))
    y_hat = clf.predict(test_x)
    print("Prediction Score is (QDA): " + str(accuracy_score(test_y, y_hat)))

    with open("results.txt", "a") as my_file:
        my_file.write("[QDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    if extra_test:
        top(clf, test_x, test_y, "QDA", extra_attempts=1)
        top(clf, test_x, test_y, "QDA", extra_attempts=3)

    if num_test_y == len(clf.classes_):
        with open("classification_reports.txt", "a") as my_file:
            my_file.write("---[QDA]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                                labels=[str(i) for i in clf.classes_],
                                                target_names=[str(i) for i in clf.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_predict=y_hat, clf=clf, clf_name='QDA')
    else:
        print("TODO")


def discriminant_load_test(test_set, test_x=None, test_y=None):
    lda = load('LDA.joblib')
    qda = load('QDA.joblib')
    if test_x is None or test_y is None:
        test_x, test_y = read_data(test_set)
    lda_test(lda, test_x, test_y)
    qda_test(qda, test_x, test_y)
