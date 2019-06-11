from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from misc import *
import time
from joblib import dump
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_fscore_support


def get_logistic(train_x, train_y, n_fold=10, slow=False):
    start = time.time()
    n = np.logspace(-3, 3)
    param_grid = {'C': n}
    log = LogisticRegression(warm_start=False, max_iter=6000, multi_class='ovr', solver='lbfgs')
    if slow:
        log_model = GridSearchCV(log, param_grid, n_jobs=-1, cv=n_fold, verbose=2)
    else:
        log_model = RandomizedSearchCV(log, param_grid, n_jobs=-1, cv=n_fold, verbose=2)
    log_model.fit(train_x, train_y)

    if slow:
        plot_grid_search(log_model.cv_results_, n, 'Logistic_Regression_Cost')
    else:
        print(n.shape)
        print(len(log_model.cv_results['mean_test_score']))

    print("[INFO] Logistic Regression-Best Parameters: " + str(log_model.best_params_))
    print("[INFO] randomized search took {:.2f} seconds".format(time.time() - start))
    print("[Logistic] Training Score is: " + str(log_model.score(train_x, train_y)))
    with open("results.txt", "a+") as my_file:
        my_file.write("[Logistic Regression] Best Parameters: " + str(log_model.best_params_) + '\n')
        my_file.write("[Logistic Regression] Training Mean Test Score: " +
                      str(log_model.score(train_x, train_y)) + '\n')
    dump(log_model, "./Classifiers/logistic.joblib")
    return log_model


def log_linear_test(clf, test_x, test_y, extra_test=False):
    num_y_test = len(np.unique(test_y))
    y_hat = clf.predict(test_x)
    print("[Logistic] Testing Score is: " + str(accuracy_score(y_true=test_y, y_pred=y_hat)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[Logistic Regression] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    if extra_test:
        top(clf, test_x, test_y, "Logistic_Regression", extra_attempts=1)
        top(clf, test_x, test_y, "Logistic_Regression", extra_attempts=3)

    if num_y_test == len(clf.classes_):
        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[Logistic Regression]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                                labels=[str(i) for i in clf.classes_],
                                                target_names=[str(i) for i in clf.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=clf, clf_name='Logistic_Regression')
    else:
        # It will crash if you don't have same number of stuff.
        # The Classification report stuff must be obtained manually
        # precision, recall, f1-score, Support
        precision_score(y_true=test_y, y_pred=y_hat, average='weighted', labels=clf.classes_)
        f1_score(y_true=test_y, y_pred=y_hat, average='weighted', labels=clf.classes_)
        recall_score(y_true=test_y, y_pred=y_hat, average='weighted', labels=clf.classes_)
        precision_recall_fscore_support(y_true=test_y, y_pred=y_hat, average='weighted', labels=clf.classes_)
