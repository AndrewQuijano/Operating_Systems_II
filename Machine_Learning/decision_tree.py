from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
from misc import *
import time
from joblib import dump


def decision_tree_raw(train_x, train_y):
    start = time.time()
    tree = DecisionTreeClassifier().fit(train_x, train_y)
    print("[INFO] Time to fit Decision tree is {:.2f} seconds".format(time.time() - start))
    return tree


def tune_tree(train_x, train_y, n_fold=10, slow=True, n_iter_search=10):
    # Minimum number of samples required to split a node
    min_samples_split = np.arange(5, 20, 1)
    # Minimum number of samples required at each leaf node
    min_samples_leaf = np.arange(5, 20, 1)
    # Maximum number of levels in tree
    max_depth = np.arange(3, 20, 1)

    random_grid = {
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'max_depth': max_depth
    }

    if slow:
        tree = GridSearchCV(estimator=DecisionTreeClassifier(), param_grid=random_grid,
                            cv=n_fold, verbose=2, n_jobs=-1)
    else:
        tree = RandomizedSearchCV(estimator=DecisionTreeClassifier(), param_distributions=random_grid,
                                  cv=n_fold, verbose=2, n_iter=n_iter_search, n_jobs=-1)
    tree.fit(train_x, train_y)
    # plot_grid_search(tree.cv_results_, min_samples_split, 'min_samples_split')
    # plot_grid_search(tree.cv_results_, min_samples_leaf, 'min_samples_leaf')
    # plot_grid_search(tree.cv_results_, max_depth, 'max_depth')
    tree.fit(train_x, train_y)
    return tree


def get_tree(train_x, train_y, test_x=None, test_y=None, n_fold=5, slow=False):
    start_time = time.time()
    tree = tune_tree(train_x, train_y, n_fold, slow)
    print("--- Best Parameter Decision Tree Time: %s seconds ---" % (time.time() - start_time))
    print("Best Decision Tree Parameters: " + str(tree.get_params()))
    print("[Decision_Tree] Training Mean Test Score: " + str(tree.score(train_x, train_y)))
    dump(tree, "tree.joblib")

    with open("results.txt", "a+") as my_file:
        my_file.write("[Decision Tree] Best Parameters: " + str(tree.get_params()) + '\n')
        my_file.write("[Decision Tree] Training Mean Test Score: " + str(tree.score(train_x, train_y)) + '\n')

    if test_x is not None or test_y is not None:
        tree_test(tree, test_x, test_y)
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in tree.classes_]))
    return tree


def tree_test(tree, test_x, test_y, extra_test=False):
    y_hat = tree.predict(test_x)
    print("[Decision_Tree] Testing Mean Test Score " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=tree, clf_name='Decision_Tree')
    # Sanity check to match with test score
    if extra_test:
        top(tree, test_x, test_y, "Decision Tree", extra_attempts=1)
        top(tree, test_x, test_y, "Decision Tree", extra_attempts=3)

    with open("results.txt", "a+") as my_file:
        my_file.write("[Decision_Tree] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[Decision Tree]---\n")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            labels=[str(i) for i in tree.classes_],
                                            target_names=[str(i) for i in tree.classes_]))
        my_file.write('\n')
