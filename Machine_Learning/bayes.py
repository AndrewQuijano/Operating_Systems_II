from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score
from misc import *
import time


# http://scikit-learn.org/stable/auto_examples/calibration/plot_calibration.html#sphx-glr-auto-examples-calibration-plot-calibration-py
def naive_bayes(train_x, train_y, n_fold=10):
    # Gaussian Naive-Bayes with no calibration
    clf = GaussianNB()
    # Gaussian Naive-Bayes with isotonic calibration
    clf_isotonic = CalibratedClassifierCV(clf, cv=n_fold, method='isotonic')
    # Gaussian Naive-Bayes with sigmoid calibration
    clf_sigmoid = CalibratedClassifierCV(clf, cv=n_fold, method='sigmoid')

    start_time = time.time()
    clf.fit(train_x, train_y)
    clf_isotonic.fit(train_x, train_y)
    clf_sigmoid.fit(train_x, train_y)
    print("--- Time to fit 3 Bayes Classifiers: %s seconds ---" % (time.time() - start_time))

    with open("results.txt", "a+") as my_file:
        my_file.write("[NB] Training Mean Test Score: " + str(clf.score(train_x, train_y)))
        my_file.write("[NB Isotonic] Training Mean Test Score: " + str(clf_isotonic.score(train_x, train_y)) + '\n')
        my_file.write("[NB Sigmoid] Training Mean Test Score: " + str(clf_sigmoid.score(train_x, train_y)))
    return clf, clf_isotonic, clf_sigmoid


def naive_bayes_test(clf, clf_isotonic, clf_sigmoid, test_x, test_y, extra_test=False):
    prob_pos_clf = clf.predict(test_x)
    prob_pos_isotonic = clf_isotonic.predict(test_x)
    prob_pos_sigmoid = clf_sigmoid.predict(test_x)

    # Evaluate Results
    # Sanity check to match with test score
    if extra_test:
        top(clf, test_x, test_y, "Naive Bayes")
        top(clf, test_x, test_y, "Naive Bayes", 3)

    with open("results.txt", "a+") as my_file:
        my_file.write("[NB] Testing Mean Test Score: " + str(accuracy_score(test_y, prob_pos_clf)))
    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[Naive Bayes]---")
        my_file.write(classification_report(y_true=test_y, y_pred=prob_pos_clf,
                                            target_names=[str(i) for i in clf.classes_]))
    # print(classification_report(test_y, prob_pos_clf, target_names=[str(i) for i in clf.classes_]))
    make_confusion_matrix(y_true=test_y, y_pred=prob_pos_clf, clf=clf, clf_name='Naive_Bayes')

    # Sanity check to match with test score
    if extra_test:
        top(clf, test_x, test_y, "Bayes with Isotonic Calibration")
        top(clf, test_x, test_y, "Bayes with Isotonic Calibration", 3)

    with open("results.txt", "a+") as my_file:
        my_file.write("[NB Isotonic] Testing Mean Test Score: " + str(accuracy_score(test_y, prob_pos_isotonic)) + '\n')
    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[Bayes with Isotonic Calibration]---\n")
        my_file.write(classification_report(y_true=test_y, y_pred=prob_pos_isotonic,
                                            target_names=[str(i) for i in clf_isotonic.classes_]))
        my_file.write('\n')
    # print(classification_report(test_y, prob_pos_isotonic, target_names=[str(i) for i in clf_isotonic.classes_]))
    make_confusion_matrix(y_true=test_y, y_pred=prob_pos_isotonic, clf=clf_isotonic, clf_name='Naive_Bayes_Isotonic')

    # Sanity check to match with test score
    if extra_test:
        top(clf, test_x, test_y, "Bayes with Sigmoid Calibration")
        top(clf, test_x, test_y, "Bayes with Sigmoid Calibration")

    with open("results.txt", "a+") as my_file:
        my_file.write("[NB Sigmoid] Testing Mean Test Score: " + str(accuracy_score(test_y, prob_pos_sigmoid)))
    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[Bayes with Sigmoid Calibration]---")
        my_file.write(classification_report(y_true=test_y, y_pred=prob_pos_sigmoid,
                                            target_names=[str(i) for i in clf_sigmoid.classes_]))
    # print(classification_report(test_y, prob_pos_sigmoid, target_names=[str(i) for i in clf_sigmoid.classes_]))
    make_confusion_matrix(y_true=test_y, y_pred=prob_pos_sigmoid, clf=clf_sigmoid, clf_name='Naive_Bayes_Sigmoid')
