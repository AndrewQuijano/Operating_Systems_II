import time
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.neighbors import KNeighborsClassifier
from misc import *
from joblib import dump


def raw_knn(train_x, train_y):
    start = time.time()
    knn = KNeighborsClassifier(n_neighbors=3).fit(train_x, train_y)
    print("[INFO] KNN fit took {:.2f} seconds".format(time.time() - start))
    return knn


# https://www.pyimagesearch.com/2016/08/15/how-to-tune-hyperparameters-with-python-and-scikit-learn/
def get_knn(train_x, train_y, test_x=None, test_y=None, n_fold=10, slow=True):
    # Get Number of features
    rows = np.shape(train_x)[0]

    if rows > 101:
        rows = 101
    else:
        rows = int((rows/2) - 1)

    # print("Highest value of k to tune up to is: " + str(rows) + " features")
    n = np.arange(3, rows, 2)
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
    # plot_grid_search(best_knn.cv_results_, n, 'KNN_n_neighbors')

    # evaluate the best randomized searched model on the testing data
    print("[INFO] KNN-Best Parameters: " + str(best_knn.best_params_))
    print("[INFO] Tuning took {:.2f} seconds".format(time.time() - start))
    print("[KNN] Training Score is: " + str(best_knn.score(train_x, train_y)))
    dump(best_knn, "knn.joblib")

    with open("results.txt", "a+") as my_file:
        my_file.write("[KNN] KNN-Best Parameters: " + str(best_knn.best_params_))
        my_file.write("[KNN] Training Mean Test Score: " + str(best_knn.score(train_x, train_y)) + '\n')

    if test_x is not None and test_y is not None:
        knn_test(best_knn, test_x, test_y)
    return best_knn


def knn_test(best_knn, test_x, test_y, extra_test=False):
    y_hat = best_knn.predict(test_x)
    print("[KNN] Testing Score is: " + str(accuracy_score(test_y, y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=best_knn, clf_name='KNN')

    if extra_test:
        top(best_knn, test_x, test_y, "KNN", extra_attempts=1)
        top(best_knn, test_x, test_y, "KNN", extra_attempts=3)

    with open("results.txt", "a+") as my_file:
        my_file.write("[KNN] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)) + '\n')
    with open("classification_reports.txt", "a+") as my_file:
        my_file.write("---[KNN]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in best_knn.classes_]))
        my_file.write('\n')
