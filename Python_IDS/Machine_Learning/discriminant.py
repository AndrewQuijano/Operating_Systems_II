from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from misc import *


def discriminant_line(train_x, train_y, test_x, test_y):
    lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
    lda.fit(train_x, train_y)
    print("Training Score (LDA): " + str(lda.score(train_x, train_y)))
    y_hat = lda.predict(test_x)
    print("Prediction Score is (LDA): " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=lda, clf_name='LDA')
    top(lda, test_x, test_y, "LDA", extra_attempts=1)
    top(lda, test_x, test_y, "LDA", extra_attempts=3)

    with open("results.txt", "a") as my_file:
        my_file.write("[LDA] Training Mean Test Score: " + str(lda.score(train_x, train_y)))
        my_file.write("[LDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[LDA]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in lda.classes_]))
    # print(classification_report(test_y, y_hat, target_names=[str(i) for i in lda.classes_]))
    return lda


def discriminant_quad(train_x, train_y, test_x, test_y):
    qda = QuadraticDiscriminantAnalysis(store_covariance=True)
    qda.fit(train_x, train_y)
    print("Training Score is (QDA): " + str(qda.score(train_x, train_y)))
    y_hat = qda.predict(test_x)
    print("Prediction Score is (QDA): " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=qda, clf_name='QDA')
    top(qda, test_x, test_y, "QDA", extra_rooms=1)
    top(qda, test_x, test_y, "QDA", extra_rooms=3)

    with open("results.txt", "a") as my_file:
        my_file.write("[QDA] Training Mean Test Score: " + str(qda.score(train_x, train_y)) + '\n')
        my_file.write("[QDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[QDA]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in qda.classes_]))
        my_file.write('\n')
    # print(classification_report(test_y, y_hat, target_names=[str(i) for i in qda.classes_]))
    return qda
