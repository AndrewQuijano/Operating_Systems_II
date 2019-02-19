from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score
from generic import *


# http://scikit-learn.org/stable/auto_examples/calibration/plot_calibration.html#sphx-glr-auto-examples-calibration-plot-calibration-py
def naive_bayes(train_x, train_y, test_x, test_y, n_fold=10):
    # Gaussian Naive-Bayes with no calibration
    clf = GaussianNB()
    clf.fit(train_x, train_y)  # GaussianNB itself does not support sample-weights
    prob_pos_clf = clf.predict(test_x)

    # Gaussian Naive-Bayes with isotonic calibration
    clf_isotonic = CalibratedClassifierCV(clf, cv=n_fold, method='isotonic')
    clf_isotonic.fit(train_x, train_y)
    prob_pos_isotonic = clf_isotonic.predict(test_x)

    # Gaussian Naive-Bayes with sigmoid calibration
    clf_sigmoid = CalibratedClassifierCV(clf, cv=n_fold, method='sigmoid')
    clf_sigmoid.fit(train_x, train_y)
    prob_pos_sigmoid = clf_sigmoid.predict(test_x)

    y_hat = clf.score(test_x, test_y)
    print("No calibration Test Error: %1.3f" % y_hat)
    with open("results.txt", "a") as my_file:
        my_file.write("[NB] Training Mean Test Score: " + str(clf.score(train_x, train_y)))
        my_file.write("[NB] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Decision Tree]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in clf.classes_]))
    # print(classification_report(test_y, prob_pos_clf, target_names=[str(i) for i in clf.classes_]))
    make_confusion_matrix(y_true=test_y, y_pred=prob_pos_clf, clf=clf, clf_name='Naive_Bayes')

    y_hat = clf_isotonic.score(test_x, test_y)
    print("With isotonic calibration Test Error: %1.3f" % y_hat)
    with open("results.txt", "a") as my_file:
        my_file.write("[NB Isotonic] Training Mean Test Score: " + str(clf_isotonic.score(train_x, train_y)))
        my_file.write("[NB Isotonic] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Decision Tree]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in clf_isotonic.classes_]))
    # print(classification_report(test_y, prob_pos_isotonic, target_names=[str(i) for i in clf_isotonic.classes_]))
    make_confusion_matrix(y_true=test_y, y_pred=prob_pos_isotonic, clf=clf_isotonic, clf_name='Naive_Bayes_Isotonic')

    y_hat = clf_sigmoid.score(test_x, test_y)
    print("With sigmoid calibration Test Error: %1.3f" % y_hat)
    with open("results.txt", "a") as my_file:
        my_file.write("[NB Sigmoid] Training Mean Test Score: " + str(clf_sigmoid.score(train_x, train_y)))
        my_file.write("[NB Sigmoid] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Decision Tree]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in clf_sigmoid.classes_]))
    # print(classification_report(test_y, prob_pos_sigmoid, target_names=[str(i) for i in clf_sigmoid.classes_]))
    make_confusion_matrix(y_true=test_y, y_pred=prob_pos_sigmoid, clf=clf_sigmoid, clf_name='Naive_Bayes_Sigmoid')
    return clf, clf_isotonic, clf_sigmoid


def main():
    # Read Wifi and Blue Tooth Data Set
    blue_x, blue_y = read_data_set('./blue.csv')
    wifi_x, wifi_y = read_data_set('./wifi.csv')

    # Build your CV sets here
    blue_train_x, blue_train_y, blue_test_x, blue_test_y = get_cv_set(blue_x, blue_y)
    wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y = get_cv_set(wifi_x, wifi_y)

    blue_clf = naive_bayes(blue_train_x, blue_train_y, blue_test_x, blue_train_y)
    wifi_clf = naive_bayes(wifi_train_x, wifi_train_y, wifi_test_x, wifi_train_y)


if __name__ == "__main__":
    main()