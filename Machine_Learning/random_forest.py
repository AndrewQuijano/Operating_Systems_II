from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from misc import *
import time


def get_forest(train_x, train_y, test_x=None, test_y=None, n_fold=10, slow=False):
    start_time = time.time()
    best_forest = tune_forest(train_x, train_y, n_fold, slow)
    print("--- Best Parameter Random Forest Time: %s seconds ---" % (time.time() - start_time))
    print("Best Random Forest Parameters: " + str(best_forest.get_params()))
    print("[Random_Forest]Training Mean Test Score: " + str(best_forest.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[Random_Forest] Best Parameters: " + str(best_forest.get_params()) + '\n')
        my_file.write("[Random_Forest] Training Mean Test Score: " + str(best_forest.score(train_x, train_y)) + '\n')

    if test_x is not None and test_y is not None:
        forest_test(best_forest, test_x, test_y)
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

    # random_grid = {
    #    'n_estimators': n_estimators,
    #    'max_features': max_features,
    #    'max_depth': max_depth,
    #    'min_samples_split': min_samples_split,
    #    'min_samples_leaf': min_samples_leaf,
    #    }

    # Step 1: Use the random grid to search for best hyper parameters
    # First create the base model to tune
    rf = RandomForestClassifier(warm_start=False, n_estimators=100)
    if slow:
        rf_estimate = GridSearchCV(estimator=rf, param_grid={'n_estimators': n_estimators}, cv=n_fold, n_jobs=-1)
    else:
        rf_estimate = RandomizedSearchCV(estimator=rf, param_distributions={'n_estimators': n_estimators},
                                         cv=n_fold, n_jobs=-1)
    rf_estimate.fit(train_features, train_labels)
    plot_grid_search(rf_estimate.cv_results_, n_estimators, 'n_estimators')

    rf = RandomForestClassifier(warm_start=False, n_estimators=100)
    if slow:
        rf_max = GridSearchCV(estimator=rf, param_grid={'max_features': max_features},
                              cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    else:
        rf_max = RandomizedSearchCV(estimator=rf, param_distributions={'max_features': max_features},
                                    cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    rf_max.fit(train_features, train_labels)
    plot_grid_search(rf_max.cv_results_, max_features, 'max_features')

    rf = RandomForestClassifier(warm_start=False, n_estimators=100)
    if slow:
        rf_distro = GridSearchCV(estimator=rf, param_grid={'max_depth': max_depth}, cv=n_fold, n_jobs=-1)
    else:
        rf_distro = RandomizedSearchCV(estimator=rf, param_distributions={'max_depth': max_depth},
                                       cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    rf_distro.fit(train_features, train_labels)
    plot_grid_search(rf_distro.cv_results_, max_depth, 'max_depth')

    rf = RandomForestClassifier(warm_start=False, n_estimators=100)
    if slow:
        rf_min_split = GridSearchCV(estimator=rf, param_grid={'min_samples_split': min_samples_split},
                                    cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    else:
        rf_min_split = RandomizedSearchCV(estimator=rf, param_distributions={'min_samples_split': min_samples_split}
                                          , cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    rf_min_split.fit(train_features, train_labels)
    plot_grid_search(rf_min_split.cv_results_, min_samples_split, 'min_samples_split')

    rf = RandomForestClassifier(warm_start=False, n_estimators=100)
    if slow:
        rf_min_leaf = GridSearchCV(estimator=rf, param_grid={'min_samples_leaf': min_samples_leaf},
                                   cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    else:
        rf_min_leaf = RandomizedSearchCV(estimator=rf, param_distributions={'min_samples_leaf': min_samples_leaf},
                                         cv=n_fold, n_jobs=-1, pre_dispatch='2*n_jobs')
    rf_min_leaf.fit(train_features, train_labels)
    plot_grid_search(rf_min_leaf.cv_results_, min_samples_leaf, 'min_samples_leaf')

    random_forest = RandomForestClassifier(warm_start=False,
                                           n_estimators=rf_estimate.best_params_['n_estimators'],
                                           max_features=rf_max.best_params_['max_features'],
                                           max_depth=rf_distro.best_params_['max_depth'],
                                           min_samples_split=rf_min_split.best_params_['min_samples_split'],
                                           min_samples_leaf=rf_min_leaf.best_params_['min_samples_leaf'])
    random_forest.fit(train_features, train_labels)
    return random_forest


def forest_test(best_forest, test_x, test_y, extra_test=False):
    y_hat = best_forest.predict(test_x)
    print("[Random_Forest] Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))
    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=best_forest, clf_name='Random_Forest')
    if extra_test:
        top(best_forest, test_x, test_y, "Random_Forest", extra_attempts=1)
        top(best_forest, test_x, test_y, "Random_Forest", extra_attempts=3)
    with open("results.txt", "a+") as my_file:
        my_file.write("[Random_Forest] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[Random_Forest]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in best_forest.classes_]))
        my_file.write('\n')
