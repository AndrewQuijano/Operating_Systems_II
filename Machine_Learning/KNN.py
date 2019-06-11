import time
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump
from misc import *


# https://www.pyimagesearch.com/2016/08/15/how-to-tune-hyperparameters-with-python-and-scikit-learn/
def get_knn(train_x, train_y, n_fold=10, slow=False):
    n = np.arange(3, 18, 2)
    start = time.time()
    # tune the hyper parameters via a randomized search
    if slow:
        best_knn = GridSearchCV(estimator=KNeighborsClassifier(), param_grid={'n_neighbors': n},
                                n_jobs=-1, cv=n_fold, verbose=2)
    else:
        best_knn = RandomizedSearchCV(estimator=KNeighborsClassifier(), param_distributions={'n_neighbors': n},
                                      n_jobs=-1, cv=n_fold, verbose=2)
    best_knn.fit(train_x, train_y)
    # Plot the CV-Curve
    plot_grid_search(best_knn, 'n_neighbors', 'KNN')
    print("[INFO] KNN-Best Parameters: " + str(best_knn.best_params_))
    print("[INFO] Tuning took {:.2f} seconds".format(time.time() - start))
    print("[KNN] Training Score is: " + str(best_knn.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[KNN] KNN-Best Parameters: " + str(best_knn.best_params_) + '\n')
        my_file.write("[KNN] Training Mean Test Score: " + str(best_knn.score(train_x, train_y)) + '\n')
    dump(best_knn, "./Classifiers/knn.joblib")
    return best_knn


def knn_test(best_knn, test_x, test_y, extra_test=False):
    num_test_y = len(np.unique(test_y))

    y_hat = best_knn.predict(test_x)
    print("[KNN] Testing Score is: " + str(accuracy_score(test_y, y_hat)))
    with open("results.txt", "a+") as my_file:
        my_file.write("[KNN] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')

    if extra_test:
        top(best_knn, test_x, test_y, "KNN", extra_attempts=1)
        top(best_knn, test_x, test_y, "KNN", extra_attempts=3)

    if num_test_y == len(best_knn.classes_):
        with open("classification_reports.txt", "a+") as my_file:
            my_file.write("---[KNN]---\n")
            my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                                labels=[str(i) for i in best_knn.classes_],
                                                target_names=[str(i) for i in best_knn.classes_]))
            my_file.write('\n')
        make_confusion_matrix(y_true=test_y, y_predict=y_hat, clf=best_knn, clf_name='KNN')
    else:
        print("TODO")
