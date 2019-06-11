from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.neural_network import MLPClassifier
from joblib import dump
import time
from misc import *


# http://scikit-learn.org/stable/auto_examples/neural_networks/plot_mlp_alpha.html#sphx-glr-auto-examples-neural-networks-plot-mlp-alpha-py
# http://scikit-learn.org/stable/auto_examples/neural_networks/plot_mlp_training_curves.html#sphx-glr-auto-examples-neural-networks-plot-mlp-training-curves-py
def get_brain(train_x, train_y, slow=False):
    start_time = time.time()
    clf = tune_brain(train_x, train_y, slow)
    print("--- Best Parameter NN Generation: %s seconds ---" % (time.time() - start_time))
    print("[NN] Training Mean Test Score: " + str(clf.score(train_x, train_y)))
    dump(clf, "./Classifiers/neural_network.joblib")

    with open("results.txt", "a") as my_file:
        my_file.write("[Neural_Network] Best Parameters: " + str(clf.best_params_) + '\n')
        my_file.write("[Neural_Network] Training Mean Test Score: " + str(clf.score(train_x, train_y)) + '\n')
    return clf


# Note alpha needs to grow exponentially!
def tune_brain(train_x, train_y, n_fold=10, slow=False):
    # Want to go from 0.001 to 1, but on exponential scale!
    alphas = np.logspace(start=-5, stop=0, endpoint=True, num=5)
    hidden_layer = np.arange(3, 10, 1)
    solvers = ['lbfgs', 'adam']
    param_grid = {'alpha': alphas, 'hidden_layer_sizes': hidden_layer, 'solver': solvers}

    if slow:
        clf = GridSearchCV(MLPClassifier(warm_start=False), param_grid, n_jobs=-1, cv=n_fold)
    else:
        clf = RandomizedSearchCV(MLPClassifier(warm_start=False), param_grid, n_jobs=-1, cv=n_fold)

    clf.fit(train_x, train_y)
    plot_grid_search(clf, 'alpha', 'NN')
    plot_grid_search(clf, 'hidden_layer_sizes', 'NN')
    plot_grid_search(clf, 'solver', 'NN')
    return clf


def brain_test(clf, test_x, test_y, extra_test=False):
    num_test_y = len(np.unique(test_y))
    y_hat = clf.predict(test_x)
    print("[NN] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))

    if extra_test:
        top(clf, test_x, test_y, "Neural_Network", extra_attempts=1)
        top(clf, test_x, test_y, "Neural_Network", extra_attempts=3)

    if num_test_y == len(clf.classes_):
        with open("results.txt", "a") as my_file:
            my_file.write("[Neural_Network] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

        with open("classification_reports.txt", "a") as my_file:
            my_file.write("---[Neural_Network]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                                target_names=[str(i) for i in clf.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_predict=y_hat, clf=clf, clf_name='Neural_Network')
    else:
        print("TODO")
