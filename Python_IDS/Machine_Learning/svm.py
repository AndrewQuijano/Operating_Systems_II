from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from misc import *
import time


# Default is 10...
def svc_rbf_param_selection(x, y, n_folds=10):
    c = np.arange(0.01, 1, 0.01)
    gammas = np.arange(0.01, 1, 0.01)

    # Test with just cost...
    rbf_search_cost = GridSearchCV(svm.SVC(kernel='rbf', gamma='scale'), param_grid={'C': c}, cv=n_folds,
                                   n_jobs=-1, error_score='raise')
    rbf_search_cost.fit(x, y)
    plot_grid_search(rbf_search_cost.cv_results_, c, 'SVM_RBF_Cost')

    # Test with just gamma
    rbf_search_gamma = GridSearchCV(svm.SVC(kernel='rbf'), param_grid={'gamma': gammas}, cv=n_folds,
                                    error_score='raise')
    rbf_search_gamma.fit(x, y)
    plot_grid_search(rbf_search_gamma.cv_results_, gammas, 'SVM_RBF_Gamma')

    # FINAL STEP
    model = svm.SVC(kernel='rbf', C=rbf_search_cost.best_params_['C'], gamma=rbf_search_gamma.best_params_['gamma'])
    model.fit(x, y)
    return model


# Default is 10...
def svc_linear_param_selection(x, y, n_folds=10):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'C': c}
    model = svm.SVC(kernel='linear')
    svm_line = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    svm_line.fit(x, y)
    plot_grid_search(svm_line.cv_results_, c, 'SVM_Linear_Cost')
    return svm_line


# http://scikit-learn.org/stable/modules/model_evaluation.html
def svm_linear(train_x, train_y, test_x, test_y):
    start_time = time.time()
    svm_line = svc_linear_param_selection(train_x, train_y)
    print("--- Best Parameter Linear SVM: %s seconds ---" % (time.time() - start_time))
    print("Best Linear Parameters: " + str(svm_line.best_params_))
    print("Linear SVM, Training Mean Test Score: " + str(svm_line.score(train_x, train_y)))
    y_hat = svm_line.predict(test_x)
    print("Linear SVM, Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=svm_line, clf_name='Linear_SVM')
    top(svm_line, test_x, test_y, "SVM_Linear", extra_attempts=1)
    top(svm_line, test_x, test_y, "SVM_Linear", extra_attempts=2)

    with open("results.txt", "a") as my_file:
        my_file.write("[SVM_Linear] Best Parameters: " + str(svm_line.get_params()) + '\n')
        my_file.write("[SVM Linear] Training Mean Test Score: " + str(svm_line.score(train_x, train_y)) + '\n')
        my_file.write("[SVM Linear] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[SVM Linear]---\n")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in svm_line.classes_]))
        my_file.write('\n')
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in svm_line.classes_]))
    return svm_line


def svm_rbf(train_x, train_y, test_x, test_y):
    start_time = time.time()
    svm_radial = svc_rbf_param_selection(train_x, train_y)
    print("--- Best Parameter RBF Time to complete: %s seconds ---" % (time.time() - start_time))
    print("Best RBF Parameters: " + str(svm_radial.get_params()))
    print("RBF SVM, Training Mean Test Score: " + str(svm_radial.score(train_x, train_y)))
    y_hat = svm_radial.predict(test_x)
    print("RBF SVM, Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=svm_radial, clf_name='Radial_SVM')
    top(svm_radial, test_x, test_y, "SVM_Radial", extra_attempts=1)
    top(svm_radial, test_x, test_y, "SVM_Radial", extra_attempts=2)

    with open("results.txt", "a") as my_file:
        my_file.write("[SVM_Radial] Best Parameters: " + str(svm_radial.get_params()) + '\n')
        my_file.write("[SVM Radial] Training Mean Test Score: " + str(svm_radial.score(train_x, train_y)) + '\n')
        my_file.write("[SVM Radial] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[SVM Radial]---\n")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i)
                                                                                       for i in svm_radial.classes_]))
        my_file.write('\n')
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in svm_radial.classes_]))
    return svm_radial
