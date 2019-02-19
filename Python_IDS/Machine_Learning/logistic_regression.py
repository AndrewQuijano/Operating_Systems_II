import time
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from generic import *


def logistic_linear(train_x, train_y, test_x, test_y):
    start = time.time()
    n = np.logspace(-3, 3)
    param_grid = {'C': n}
    log = LogisticRegression(warm_start=False)
    log_model = GridSearchCV(log, param_grid, n_jobs=-1)
    log_model.fit(train_x, train_y)
    plot_grid_search(log_model.cv_results_, n, 'Logistic_Regression_Cost')

    print("[INFO] Logistic Regression-Best Parameters: " + str(log_model.best_params_))
    print("[INFO] randomized search took {:.2f} seconds".format(time.time() - start))
    print("Training Score is: " + str(log_model.score(train_x, train_y)))
    y_hat = log_model.predict(test_x)
    print("Testing Score is: " + str(accuracy_score(y_true=test_y, y_pred=y_hat)))

    make_confusion_matrix(y_true=test_y, y_pred=y_hat, clf=log_model, clf_name='Logistic_Regression')
    top(log_model, test_x, test_y, extra_rooms=2)

    with open("results.txt", "a") as my_file:
        my_file.write("[Logistic Regression] Training Mean Test Score: " + str(log_model.score(train_x, train_y)))
        my_file.write("[Logistic Regression] Testing Mean Test Score: " + str(accuracy_score(test_y, y_hat)))
    with open("classification_reports.txt", "a") as my_file:
        my_file.write("---[Logistic Regression]---")
        my_file.write(classification_report(y_true=test_y, y_pred=y_hat,
                                            target_names=[str(i) for i in log_model.classes_]))
    # print(classification_report(y_true=test_y, y_pred=y_hat, target_names=[str(i) for i in log_model.classes_]))
    return log_model


def main():
    # Read Wifi and Blue Tooth Data Set
    blue_x, blue_y = read_data_set('./blue.csv')
    wifi_x, wifi_y = read_data_set('./wifi.csv')

    # Build your CV sets here
    blue_train_x, blue_train_y, blue_test_x, blue_test_y = get_cv_set(blue_x, blue_y)
    wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y = get_cv_set(wifi_x, wifi_y)

    # Test blue tooth
    blue_clf = logistic_linear(blue_train_x, blue_train_y, blue_test_x, blue_test_y)
    wifi_clf = logistic_linear(wifi_train_x, wifi_train_y, wifi_test_x, wifi_test_y)


if __name__ == "__main__":
    main()