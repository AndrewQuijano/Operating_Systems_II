import time
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from generic import *


# https://www.pyimagesearch.com/2016/08/15/how-to-tune-hyperparameters-with-python-and-scikit-learn/
def tune_knn(train_x, train_y, test_x, test_y, n_fold=10):
    # Get Number of features
    rows = np.shape(train_x)[0]
    print("There are " + str(rows) + " features")

    if rows > 101:
        rows = 101
    else:
        rows = int((rows/2) - 1)

    print("Highest value of k to tune up to is: " + str(rows) + " features")
    n = np.arange(3, rows, 2)
    param_grid = {'n_neighbors': n}
    model = KNeighborsClassifier()
    start = time.time()
    # tune the hyper parameters via a randomized search
    best_knn = GridSearchCV(model, param_grid, n_jobs=-1, cv=n_fold)
    best_knn.fit(train_x, train_y)

    # Plot the CV-Curve
    plot_grid_search(best_knn.cv_results_, n, 'KNN_n_neighbors')

    # evaluate the best randomized searched model on the testing data
    print("[INFO] KNN-Best Parameters: " + str(best_knn.best_params_))
    print("[INFO] randomized search took {:.2f} seconds".format(time.time() - start))
    print("Training Score is: " + str(best_knn.score(train_x, train_y)))
    y_hat = best_knn.predict(test_x)
    print("Testing Score is: " + str(accuracy_score(test_y, y_hat)))
    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=best_knn, clf_name='KNN')

    top(best_knn, test_x, test_y, "KNN", extra_attempts=1)
    top(best_knn, test_x, test_y, "KNN", extra_attempts=3)

    with open("results.txt", "a") as my_file:
        my_file.write("[KNN] Training Mean Test Score: " + str(best_knn.score(train_x, train_y)))
        my_file.write("[KNN] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[KNN]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in best_knn.classes_]))
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in best_knn.classes_]))
    return best_knn
