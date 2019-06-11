from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score
from misc import *
import time
from joblib import dump, load


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
        my_file.write("[NB] Training Mean Test Score: " + str(clf.score(train_x, train_y)) + '\n')
        my_file.write("[NB Isotonic] Training Mean Test Score: " + str(clf_isotonic.score(train_x, train_y)) + '\n')
        my_file.write("[NB Sigmoid] Training Mean Test Score: " + str(clf_sigmoid.score(train_x, train_y)) + '\n')
    dump(clf, "./Classifiers/naive_bayes.joblib")
    dump(clf_sigmoid, "./Classifiers/NB_Sig.joblib")
    dump(clf_isotonic, "./Classifiers/NB_Isotonic.joblib")
    return clf, clf_isotonic, clf_sigmoid


def naive_bayes_test(clf, clf_isotonic, clf_sigmoid, test_x, test_y, extra_test=False):
    num_test_y = len(np.unique(test_y))
    prob_pos_clf = clf.predict(test_x)
    prob_pos_isotonic = clf_isotonic.predict(test_x)
    prob_pos_sigmoid = clf_sigmoid.predict(test_x)

    if extra_test:
        top(clf, test_x, test_y, "Naive Bayes")
        top(clf_isotonic, test_x, test_y, "Bayes with Isotonic Calibration")
        top(clf_sigmoid, test_x, test_y, "Bayes with Sigmoid Calibration")
        top(clf, test_x, test_y, "Naive Bayes", 3)
        top(clf_isotonic, test_x, test_y, "Bayes with Isotonic Calibration", 3)
        top(clf_sigmoid, test_x, test_y, "Bayes with Sigmoid Calibration", 3)

    with open("results.txt", "a+") as my_file:
        my_file.write("[NB] Testing Mean Test Score: " + str(accuracy_score(test_y, prob_pos_clf)) + '\n')
        my_file.write("[NB Isotonic] Testing Mean Test Score: " + str(accuracy_score(test_y, prob_pos_isotonic)) + '\n')
        my_file.write("[NB Sigmoid] Testing Mean Test Score: " + str(accuracy_score(test_y, prob_pos_sigmoid)) + '\n')

    if num_test_y == len(clf.classes_):
        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[Bayes with Sigmoid Calibration]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=prob_pos_sigmoid,
                                                labels=[str(i) for i in clf_sigmoid.classes_],
                                                target_names=[str(i) for i in clf_sigmoid.classes_]))
            my_file.write('\n')

        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[Bayes with Isotonic Calibration]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=prob_pos_isotonic,
                                                labels=[str(i) for i in clf_isotonic.classes_],
                                                target_names=[str(i) for i in clf_isotonic.classes_]))
            my_file.write('\n')

        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[Naive Bayes]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=prob_pos_clf,
                                                labels=[str(i) for i in clf.classes_],
                                                target_names=[str(i) for i in clf.classes]))
            my_file.write('\n')

        make_confusion_matrix(y_true=test_y, y_pred=prob_pos_clf, clf=clf, clf_name='Naive_Bayes')
        make_confusion_matrix(y_true=test_y, y_pred=prob_pos_isotonic, clf=clf_isotonic, clf_name='Naive_Bayes_Isotonic')
        make_confusion_matrix(y_true=test_y, y_pred=prob_pos_sigmoid, clf=clf_sigmoid, clf_name='Naive_Bayes_Sigmoid')
    else:
        print("TODO")


def bayes_load_test(test_set, test_x=None, test_y=None):
    clf = load('./Classifiers/naive_bayes.joblib')
    clf_isotonic = load('./Classifiers/NB_Isotonic.joblib')
    clf_sigmoid= load('./Classifiers/NB_Sigmoid.joblib')
    if test_x is None or test_y is None:
        test_x, test_y = read_data(test_set)
    naive_bayes_test(clf, clf_isotonic, clf_sigmoid, test_x, test_y, extra_test=False)
