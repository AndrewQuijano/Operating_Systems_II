from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from misc import *
import time
from joblib import dump
# from sklearn.externals.joblib import dump


def get_forest_raw(train_x, train_y):
    start_time = time.time()
    forest = RandomForestClassifier(warm_start=False, n_estimators=100).fit(train_x, train_y)
    print("--- Random Forest fit time: %s seconds ---" % (time.time() - start_time))
    return forest


def get_forest(train_x, train_y, n_fold=10, slow=False):
    start_time = time.time()
    best_forest = tune_forest(train_x, train_y, n_fold, slow)
    print("--- Best Parameter Random Forest Time: %s seconds ---" % (time.time() - start_time))
    print("Best Random Forest Parameters: " + str(best_forest.get_params()))
    print("[Random_Forest]Training Mean Test Score: " + str(best_forest.score(train_x, train_y)))
    with open("results.txt", "a+") as my_file:
        my_file.write("[Random_Forest] Best Parameters: " + str(best_forest.best_params_) + '\n')
        my_file.write("[Random_Forest] Training Mean Test Score: " + str(best_forest.score(train_x, train_y)) + '\n')
    dump(best_forest, "random_forest.joblib")
    return best_forest


# Citation:
# https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74
# http://scikit-learn.org/stable/auto_examples/model_selection/plot_randomized_search.html#sphx-glr-auto-examples-model-selection-plot-randomized-search-py
# https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
def tune_forest(train_features, train_labels, n_fold=10, slow=True):
    # Number of trees in random forest
    n_estimators = np.arange(10, 510, 10)
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = np.arange(3, 20, 1)
    # Minimum number of samples required to split a node
    min_samples_split = np.arange(5, 20, 1)
    # Minimum number of samples required at each leaf node
    min_samples_leaf = np.arange(5, 20, 1)

    random_grid = {
        'n_estimators': n_estimators,
        'max_features': max_features,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
    }

    # Step 1: Use the random grid to search for best hyper parameters
    # First create the base model to tune
    rf = RandomForestClassifier(warm_start=False, n_estimators=100)
    if slow:
        tune_rf = GridSearchCV(estimator=rf, param_grid=random_grid, cv=n_fold, n_jobs=-1, verbose=2)
    else:
        tune_rf = RandomizedSearchCV(estimator=rf, param_distributions=random_grid,
                                     cv=n_fold, n_jobs=-1, verbose=2)
    tune_rf.fit(train_features, train_labels)
    # plot_grid_search(rf_estimate.cv_results_, n_estimators, 'n_estimators')
    # plot_grid_search(rf_max.cv_results_, max_features, 'max_features')
    # plot_grid_search(rf_distro.cv_results_, max_depth, 'max_depth')
    # plot_grid_search(rf_min_split.cv_results_, min_samples_split, 'min_samples_split')
    # plot_grid_search(rf_min_leaf.cv_results_, min_samples_leaf, 'min_samples_leaf')
    return tune_rf


def forest_test(best_forest, test_x, test_y, extra_test=False):
    num_test_y = len(np.unique(test_y))
    y_hat = best_forest.predict(test_x)
    print("[Random_Forest] Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))
    with open("results.txt", "a+") as my_file:
        my_file.write("[Random_Forest] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    if extra_test:
        top(best_forest, test_x, test_y, "Random_Forest", extra_attempts=1)
        top(best_forest, test_x, test_y, "Random_Forest", extra_attempts=3)

    if num_test_y == len(best_forest.classes_):
        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[Random_Forest]---")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            labels=[str(i) for i in best_forest.classes_],
                                            target_names=[str(i) for i in best_forest.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=best_forest, clf_name='Random_Forest')
    else:
        print("TODO")
