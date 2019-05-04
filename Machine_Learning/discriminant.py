from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from misc import *
import time
from joblib import dump


def discriminant_line(train_x, train_y, test_x=None, test_y=None):
    lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
    start_time = time.time()
    lda.fit(train_x, train_y)
    print("--- Time to fit LDA: %s seconds ---" % (time.time() - start_time))
    print("Training Score (LDA): " + str(lda.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[LDA] Best Parameters: " + str(lda.get_params()) + '\n')
        my_file.write("[LDA] Training Mean Test Score: " + str(lda.score(train_x, train_y)) + '\n')
    dump(lda, "LDA.joblib")

    if test_x is not None and test_y is not None:
        lda_test(lda, test_x, test_y)
    return lda


def lda_test(lda, test_x, test_y, extra_test=False):
    y_hat = lda.predict(test_x)
    print("Testing Score is (LDA): " + str(accuracy_score(test_y, y_hat)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[LDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[LDA]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            labels=[str(i) for i in lda.classes_],
                                            target_names=[str(i) for i in lda.classes_]))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=lda, clf_name='LDA')

    if extra_test:
        top(lda, test_x, test_y, "LDA", extra_attempts=1)
        top(lda, test_x, test_y, "LDA", extra_attempts=3)


def discriminant_quad(train_x, train_y, test_x=None, test_y=None):
    qda = QuadraticDiscriminantAnalysis(store_covariance=False)
    start_time = time.time()
    qda.fit(train_x, train_y)
    print("--- Time to fit QDA: %s seconds ---" % (time.time() - start_time))
    print("Training Score is (QDA): " + str(qda.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[QDA] Best Parameters: " + str(qda.get_params()) + '\n')
        my_file.write("[QDA] Training Mean Test Score: " + str(qda.score(train_x, train_y)) + '\n')
    dump(qda, "QDA.joblib")
    if test_x is not None and test_y is not None:
        qda_test(qda, test_x, test_y)
    return qda


def qda_test(qda, test_x, test_y, extra_test=False):
    y_hat = qda.predict(test_x)
    print("Prediction Score is (QDA): " + str(accuracy_score(test_y, y_hat)))
    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=qda, clf_name='QDA')

    if extra_test:
        top(qda, test_x, test_y, "QDA", extra_attempts=1)
        top(qda, test_x, test_y, "QDA", extra_attempts=3)

    with open("results.txt", "a") as my_file:
        my_file.write("[QDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[QDA]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            labels=[str(i) for i in qda.classes_],
                                            target_names=[str(i) for i in qda.classes_]))
        my_file.write('\n')
