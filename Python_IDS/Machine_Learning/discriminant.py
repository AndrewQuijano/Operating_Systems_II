from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from generic import *


def discriminant_line(train_x, train_y, test_x, test_y):
    lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
    lda.fit(train_x, train_y)
    print("Training Score (LDA): " + str(lda.score(train_x, train_y)))
    y_hat = lda.predict(test_x)
    print("Prediction Score is (LDA): " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=lda, clf_name='LDA')
    top(lda, test_x, test_y, extra_rooms=2)

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
    top(qda, test_x, test_y, extra_rooms=2)

    with open("results.txt", "a") as my_file:
        my_file.write("[QDA] Training Mean Test Score: " + str(qda.score(train_x, train_y)))
        my_file.write("[QDA] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[QDA]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in qda.classes_]))
    # print(classification_report(test_y, y_hat, target_names=[str(i) for i in qda.classes_]))
    return qda


def main():
    blue_x, blue_y = read_data_set('./blue.csv')
    wifi_x, wifi_y = read_data_set('./wifi.csv')

    # Build your CV sets here
    blue_train_x, blue_train_y, blue_test_x, blue_test_y = get_cv_set(blue_x, blue_y)
    wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y = get_cv_set(wifi_x, wifi_y)

    fixed_blue_train_x, fixed_blue_test_x = scale_and_pca(blue_train_x, blue_test_x)
    fixed_wifi_train_x, fixed_wifi_test_x = scale_and_pca(wifi_train_x, wifi_test_x)

    blue_lda = discriminant_line(fixed_blue_train_x, blue_train_y, fixed_blue_test_x, blue_test_y)
    blue_qda = discriminant_quad(blue_train_x, blue_train_y, blue_test_x, blue_test_y)

    wifi_lda = discriminant_line(fixed_wifi_train_x, wifi_train_y, fixed_wifi_test_x, wifi_test_y)
    wifi_qda = discriminant_quad(wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y)


if __name__ == "__main__":
    main()