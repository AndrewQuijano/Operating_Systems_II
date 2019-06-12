from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from misc import *
import time
from joblib import dump


def tune_tree(train_x, train_y, n_fold=10, slow=False, n_iter_search=10):
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
    plot_grid_search(tree, 'min_samples_split', 'Decision_Tree')
    plot_grid_search(tree, 'min_samples_leaf', 'Decision_Tree')
    plot_grid_search(tree, 'max_depth', 'Decision_Tree')
    return tree


def get_tree(train_x, train_y, n_fold=10, slow=False):
    start_time = time.time()
    tree = tune_tree(train_x, train_y, n_fold, slow)
    print("--- Best Parameter Decision Tree Time: %s seconds ---" % (time.time() - start_time))
    print("Best Decision Tree Parameters: " + str(tree.best_params_))
    print("[Decision_Tree] Training Mean Test Score: " + str(tree.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[Decision Tree] Best Parameters: " + str(tree.best_params_) + '\n')
        my_file.write("[Decision Tree] Training Mean Test Score: " + str(tree.score(train_x, train_y)) + '\n')
    dump(tree, "./Classifiers/Decision_Tree.joblib")
    return tree
