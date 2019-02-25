from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from misc import *
import time


def tune_tree(train_features, train_labels, n_fold=10):
    # Minimum number of samples required to split a node
    min_samples_split = np.arange(5, 20, 1)
    # Minimum number of samples required at each leaf node
    min_samples_leaf = np.arange(5, 20, 1)
    # Maximum number of levels in tree
    max_depth = np.arange(3, 20, 1)

    # Tune min split, taken from Random Forest
    rf_min_split = GridSearchCV(estimator=DecisionTreeClassifier(), param_grid={'min_samples_split': min_samples_split},
                                cv=n_fold, verbose=2, n_jobs=-1)
    rf_min_split.fit(train_features, train_labels)
    plot_grid_search(rf_min_split.cv_results_, min_samples_split, 'min_samples_split')

    # Tune min_sample_leaf, taken from Random Forest
    rf_min_leaf = GridSearchCV(estimator=DecisionTreeClassifier(), param_grid={'min_samples_leaf': min_samples_leaf},
                               cv=n_fold, verbose=2,  n_jobs=-1)
    rf_min_leaf.fit(train_features, train_labels)
    plot_grid_search(rf_min_leaf.cv_results_, min_samples_leaf, 'min_samples_leaf')

    rf_distro = GridSearchCV(estimator=DecisionTreeClassifier(), param_grid={'max_depth': max_depth}, cv=n_fold, verbose=2, n_jobs=-1)
    rf_distro.fit(train_features, train_labels)
    plot_grid_search(rf_distro.cv_results_, max_depth, 'max_depth')

    # Build the classifier with all tuned parameters!
    # For the Project I am using this code, I should use entropy
    clf = DecisionTreeClassifier(criterion="entropy",
                                 max_depth=rf_distro.best_params_['max_depth'],
                                 min_samples_split=rf_min_split.best_params_['min_samples_split'],
                                 min_samples_leaf=rf_min_leaf.best_params_['min_samples_leaf'])
    return clf


def get_tree(train_x, train_y, test_x, test_y):
    start_time = time.time()
    tree = tune_tree(train_x, train_y)
    print("--- Best Parameter Decision Tree Time: %s seconds ---" % (time.time() - start_time))
    print("Best Decision Tree Parameters: " + str(tree.get_params()))
    print("Training Mean Test Score: " + str(tree.score(train_x, train_y)))
    y_hat = tree.predict(test_x)
    print("Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=tree, clf_name='Decision_Tree')
    # Sanity check to match with test score
    top(tree, test_x, test_y, "Decision Tree", extra_attempts=1)
    top(tree, test_x, test_y, "Decision Tree", extra_attempts=3)

    with open("results.txt", "a") as my_file:
        my_file.write("[Decision Tree] Best Parameters: " + str(tree.get_params()) + '\n')
        my_file.write("[Decision Tree] Training Mean Test Score: " + str(tree.score(train_x, train_y)) + '\n')
        my_file.write("[Decision Tree] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Decision Tree]---\n")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in tree.classes_]))
        my_file.write('\n')
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in tree.classes_]))
    return tree

