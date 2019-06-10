from sklearn.metrics import accuracy_score, classification_report
from sklearn import svm
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from joblib import dump
from misc import *
import time


def svm_rbf(train_x, train_y, n_fold=10, slow=False):
    start_time = time.time()
    svm_radial = svc_rbf_param_selection(train_x, train_y, n_fold, slow)
    print("--- Best Parameter RBF Time to complete: %s seconds ---" % (time.time() - start_time))
    print("Best RBF Parameters: " + str(svm_radial.get_params()))
    print("[SVM_Radial] Training Mean Test Score: " + str(svm_radial.score(train_x, train_y)))
    with open("results.txt", "a+") as my_file:
        my_file.write("[SVM_Radial] Best Parameters: " + str(svm_radial.best_params_) + '\n')
        my_file.write("[SVM Radial] Training Mean Test Score: " + str(svm_radial.score(train_x, train_y)) + '\n')
    dump(svm_radial, "svm_rbf.joblib")
    return svm_radial


def svc_rbf_param_selection(x, y, n_folds=10, slow=False):
    c = np.arange(0.1, 1, 0.1)
    gammas = np.arange(0.1, 1, 0.1)
    random_grid = {
        'C': c,
        'gamma': gammas
    }
    if slow:
        rbf_search = GridSearchCV(svm.SVC(kernel='rbf', gamma='scale'), param_grid=random_grid, cv=n_folds,
                                  n_jobs=-1, error_score='raise', verbose=2)
    else:
        rbf_search = RandomizedSearchCV(svm.SVC(kernel='rbf', gamma='scale'), param_distributions=random_grid,
                                        cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    rbf_search.fit(x, y)
    # plot_grid_search(rbf_search_cost.cv_results_, c, 'SVM_RBF_Cost')
    # plot_grid_search(rbf_search_gamma.cv_results_, gammas, 'SVM_RBF_Gamma')
    return rbf_search


# http://scikit-learn.org/stable/modules/model_evaluation.html
def svm_linear(train_x, train_y, n_fold=10, slow=False):
    start_time = time.time()
    svm_line = svc_linear_param_selection(train_x, train_y, n_fold, slow)
    print("--- Best Parameter Linear SVM: %s seconds ---" % (time.time() - start_time))
    print("Best Linear Parameters: " + str(svm_line.best_params_))
    print("[SVM_Linear] Training Mean Test Score: " + str(svm_line.score(train_x, train_y)))
    with open("results.txt", "a+") as my_file:
        my_file.write("[SVM_Linear] Best Parameters: " + str(svm_line.best_params_) + '\n')
        my_file.write("[SVM_Linear] Training Mean Test Score: " + str(svm_line.score(train_x, train_y)) + '\n')
    dump(svm_line, "svm_line.joblib")
    return svm_line


def svc_linear_param_selection(x, y, n_folds=10, slow=False):
    c = np.arange(0.1, 1, 0.1)
    param_grid = {'C': c}
    model = svm.SVC(kernel='linear')
    if slow:
        svm_line = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        svm_line = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    svm_line.fit(x, y)
    # plot_grid_search(svm_line.cv_results_, c, 'SVM_Linear_Cost')
    return svm_line


def svm_test(svm_clf, test_x, test_y, kernel, extra_test=False):
    num_test_y = len(np.unique(test_y))
    y_hat = svm_clf.predict(test_x)
    print("[SVM_" + kernel + "] Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[SVM_" + kernel + "] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    if extra_test:
        top(svm_clf, test_x, test_y, "SVM_" + str(kernel), extra_attempts=1)
        top(svm_clf, test_x, test_y, "SVM_" + str(kernel), extra_attempts=2)

    if num_test_y == len(svm_clf.classes_):
        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[SVM_" + str(kernel) + "]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                                labels=[str(i) for i in svm.classes_],
                                                target_names=[str(i) for i in svm_clf.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=svm_clf, clf_name='SVM_' + str(kernel))
    else:
        print("TODO")
