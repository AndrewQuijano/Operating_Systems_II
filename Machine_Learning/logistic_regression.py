from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from misc import *
import time


def logistic_linear(train_x, train_y, test_x=None, test_y=None, n_fold=10, slow=True):
    start = time.time()
    n = np.logspace(-3, 3)
    param_grid = {'C': n}
    log = LogisticRegression(warm_start=False, max_iter=1000, multi_class='auto', solver='lbfgs')
    if slow:
        log_model = GridSearchCV(log, param_grid, n_jobs=-1, cv=n_fold, pre_dispatch='2*n_jobs', verbose=2)
    else:
        log_model = RandomizedSearchCV(log, param_grid, n_jobs=-1, cv=n_fold, pre_dispatch='2*n_jobs', verbose=2)
    log_model.fit(train_x, train_y)
    plot_grid_search(log_model.cv_results_, n, 'Logistic_Regression_Cost')

    print("[INFO] Logistic Regression-Best Parameters: " + str(log_model.best_params_))
    print("[INFO] randomized search took {:.2f} seconds".format(time.time() - start))
    print("[Logistic] Training Score is: " + str(log_model.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[Logistic Regression] Best Parameters: " + str(log_model.get_params()) + '\n')
        my_file.write("[Logistic Regression] Training Mean Test Score: " +
                      str(log_model.score(train_x, train_y)) + '\n')

    if test_x is not None and test_y is not None:
        log_linear_test(log_model, test_x, test_y)
    return log_model


def log_linear_test(log_model, test_x, test_y, extra_test=False):
    y_hat = log_model.predict(test_x)
    print("[Logistic] Testing Score is: " + str(accuracy_score(y_true=test_y, y_pred=y_hat)))
    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=log_model, clf_name='Logistic_Regression')

    if extra_test:
        top(log_model, test_x, test_y, "Logistic_Regression", extra_attempts=1)
        top(log_model, test_x, test_y, "Logistic_Regression", extra_attempts=3)

    with open("results.txt", "a+") as my_file:
        my_file.write("[Logistic Regression] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[Logistic Regression]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in log_model.classes_]))
        my_file.write('\n')
