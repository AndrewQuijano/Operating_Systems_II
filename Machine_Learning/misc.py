import itertools
import numpy as np
import random
from os import mkdir, path, remove
from shutil import rmtree
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import validation_curve
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from collections import Counter
import pandas as pd
from data_set_manipulation import n_col
import scikitplot as skplt


# After a lot of tinkering around, it is always best to have your classes be strings
# for easier usage with Classification Reports and stuff.
def read_data(file, has_header=False):
    columns = n_col(file)
    if has_header:
        features = np.genfromtxt(file, delimiter=',', skip_header=1, dtype=float,
                                 autostrip=True, usecols=[i for i in range(1, columns)])
        classes = np.genfromtxt(file, delimiter=',', skip_header=1, dtype=str,
                                autostrip=True, usecols=[0])
    else:
        features = np.genfromtxt(file, delimiter=',', skip_header=0, dtype=float,
                                 autostrip=True, usecols=[i for i in range(1, columns)])
        classes = np.genfromtxt(file, delimiter=',', skip_header=0, dtype=str,
                                autostrip=True, usecols=[0])
    return features, classes


# KDD without content has 27 columns
def read_data_pandas(file_name):
    col = n_col(file_name)
    x = pd.read_csv(file_name, usecols=[i for i in range(1, col + 1)])
    y = pd.read_csv(file_name, usecols=[0])
    x = x.to_numpy()
    y = y.to_numpy()
    return x, y


def summation(elements):
    answer = 0
    for i in range(len(elements)):
        answer += elements[i]
    return answer


def is_valid_file_type(file):
    if not path.exists(file):
        return False
    if not path.isfile(file):
        return False
    return file.lower().endswith(('.csv', '.txt'))


def mean(elements):
    numerator = summation(elements)
    return numerator/len(elements)


def std_dev(elements):
    miu = mean(elements)
    variance = 0
    for i in range(len(elements)):
        variance += (elements[i] - miu) * (elements[i] - miu)
    variance = variance/len(elements)
    return variance


# Input: A file with numbers with frequencies:
# For example a List of Exam Scores:
# 80, 90, 100, 90, 75, ...
# Get <90, 2> <80, 1>, <90, 1>, in a dictionary to be used
def frequency_count(filename):
    # Read the input file into one long list
    objects = []
    with open(filename, 'r') as read_row:
        for row in read_row:
            objects.append(row)
    counter = Counter(objects)
    return dict(counter)


# Input: A Hash Map <K, V> Key is item, Value is Frequency
# Plot a Histogram!
def frequency_histogram(hash_map):
    fig, ax = plt.subplots()
    rects = ax.bar(list(hash_map.keys()), hash_map.values(), color='g')
    ax.set_xlabel('elements')
    ax.set_ylabel('count')
    ax.set_title('Frequency histogram')

    def autolabel(rectangles, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
          """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rectangles:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

    autolabel(rects)
    plt.savefig(str('./histogram.png'))
    plt.show()
    plt.close()


def dual_frequency_histogram(hash_map1, hash_map2):
    fig, ax = plt.subplots()

    ind1 = np.arange(len(hash_map1.keys()))  # the x locations for the groups
    ind2 = np.arange(len(hash_map2.keys()))
    width = 0.40  # the width of the bars

    rects1 = ax.bar(ind1 - width/2, hash_map1.values(), width=width, color='g', label='Normal')
    rects2 = ax.bar(ind2 + width/2, hash_map2.values(), width=width, color='b', label='Anomalous')

    ax.set_xlabel('Land Flag')
    ax.set_ylabel('Number of Connections')
    ax.set_xticks(ind2)
    ax.set_xticklabels(tuple(hash_map1.keys))
#    ax.set_xticklabels(('ICMP', 'TCP', 'UDP'))
#    ax.set_xticklabels(('OTH', 'REJ', 'RSTO', 'RSTOS0', 'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH'))
#    ax.set_xticklabels(("SF", "S2", "S1", "S3", "OTH", "REJ", "RSTO", "S0", "RSTR", "RSTOS0", "SH"))
    ax.set_title('Land Distribution')
    ax.legend()

    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
          """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    plt.savefig(str('./histogram.png'))
    plt.show()
    plt.close()


def plot_roc(y_test, y_hat):
    skplt.metrics.plot_roc_curve(y_test, y_hat)
    plt.show()


def get_cv_set(training_set, test_set, percentile=0.2):
    row = np.shape(training_set)[0]
    col = np.shape(training_set)[1]
    sample_idx = random.sample(range(row), int(percentile * row))

    # Get your CV data
    cv_train = training_set[sample_idx[:], 0:col]
    cv_test = test_set[sample_idx[:]]

    # Remove CV data from original
    set_diff = np.setdiff1d(np.arange(row), sample_idx)
    training_set = training_set[set_diff[:], 0:col]
    test_set = test_set[set_diff[:]]
    return training_set, test_set, cv_train, cv_test


# Technically setting the extra attempts = 1 should be equivalent to getting you the test score
def top(clf, test_x, test_y, classifier, extra_attempts=1):
    # Get your list of classes
    # Sort it such that highest probabilities come first...
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    # To print highest first, set reverse=True
    probability_dict = []
    for i in range(len(test_y)):
        if hasattr(clf, 'decision_function'):
            probability_dict.append(dict(zip(clf.classes_, clf.decision_function(test_x)[i])))
        else:
            probability_dict.append(dict(zip(clf.classes_, clf.predict_proba(test_x)[i])))
        probability_dict[i] = sorted([(v, k) for k, v in probability_dict[i].items()], reverse=True)

    success = 0
    # Let us say test the first 3 rooms? See if it matches!
    for i in range(len(test_y)):
        # print(probability_dict[i])
        for j in range(extra_attempts):
            if probability_dict[i][j][1] == test_y[i]:
                success = success + 1
                break

    # Print Results
    score = success/len(test_y)
    with open("results.txt", "a") as my_file:
        my_file.write("[" + classifier + "] Testing Mean Test Score with " + str(extra_attempts)
                      + ": " + str(score))
    # print("Test Error for " + str(extra_rooms) + " Rooms: " + str(success/len(test_y)))


def scale(train_x, test_x):
    scalar = StandardScaler()
    # Don't cheat - fit only on training data
    scalar.fit(train_x)
    x_train = scalar.transform(train_x)
    # apply same transformation to test data
    x_test = scalar.transform(test_x)
    return x_train, x_test


# If the data is co-linear you must use PCA
# Hopefully this function should get the PCA the explains up to 90% variance minimum
def scale_and_pca(train_x, test_x):
    scaled_train_x, scaled_test_x = scale(train_x, test_x)
    pr_comp = PCA(n_components=0.99, svd_solver='full')
    pr_comp.fit(scaled_train_x)
    return pr_comp.transform(scaled_train_x), pr_comp.transform(scaled_test_x)


def plot_grid_search(clf, grid_param, name_param, directory="Cross_Validation"):
    # Get Test Scores Mean
    # Get the specific parameter to compare with CV
    scores_mean = clf.cv_results_['mean_test_score']
    parameters = clf.cv_results_['param_' + name_param]
    print(parameters)
    print(len(parameters))
    print(len(scores_mean))
    scores_mean = np.array(scores_mean).reshape(len(parameters), 1)

    # Param1 is the X-axis, Param 2 is represented as a different curve (color line)
    _, ax = plt.subplots(1, 1)
    ax.plot(parameters, scores_mean, label="CV-Curve")
    ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
    ax.set_xlabel(name_param, fontsize=16)
    ax.set_ylabel('CV Average Score', fontsize=16)
    ax.legend(loc="best", fontsize=15)
    ax.grid(True)
    plt.savefig(str('./' + directory + '/CV_Plot_' + name_param + '.png'))
    plt.close()


# METHOD IS NOT USED AT THE MOMENT!
def plot_validation_curve(x, y, param_range, param_name, clf, clf_name):
    train_scores, test_scores = validation_curve(
        clf, x, y, param_name=param_name, param_range=param_range,
        cv=10, scoring="accuracy", n_jobs=-1)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.title("Validation Curve with " + clf_name)
    plt.xlabel(param_name)
    plt.ylabel("Score")
    plt.ylim(0.0, 1.1)
    lw = 2
    plt.semilogx(param_range, train_scores_mean, label="Training score",
                 color="darkorange", lw=lw)
    plt.fill_between(param_range, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.2,
                     color="darkorange", lw=lw)
    plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
                 color="navy", lw=lw)
    plt.fill_between(param_range, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.2,
                     color="navy", lw=lw)
    plt.legend(loc="best")


# Source code from:
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #    print("Normalized confusion matrix")
    # else:
    #    print('Confusion matrix, without normalization')
    # print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def make_confusion_matrix(y_true, y_predict, clf, clf_name, directory="Confusion_Matrix"):
    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_true, y_predict, labels=[str(i) for i in clf.classes_])
    np.set_printoptions(precision=2)
    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=[str(i) for i in clf.classes_], normalize=False,
                          title='Confusion matrix, without normalization: ')
    plt.savefig(str('./' + directory + '/Normalized_Confusion_Matrix_' + clf_name + '.png'))
    # plt.show()
    plt.close()

    # Plot normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=[str(i) for i in clf.classes_], normalize=True,
                          title='Normalized confusion matrix')
    plt.savefig(str('./' + directory + '/Normalized_Confusion_Matrix_' + clf_name + '.png'))
    # plt.show()
    plt.close()


def start_and_clean_up():
    try:
        # Now give user an option to delete everything and start
        # OR discontinue
        if check_files():
            # Read input from user
            args = input("Files Found! Delete them and run script? If so, press CTRL-D.\n "
                         "Otherwise, press any key to exit!")
            if args is not None:
                exit(0)
    except EOFError:
        # 3- If approved to delete, Remove it now!
        if path.exists("./results.txt") and path.isfile("./results.txt"):
            remove("./results.txt")
        if path.exists("./classification_reports.txt") and path.isfile("./classification_reports.txt"):
            remove("./classification_reports.txt")
        rmtree("./Cross_Validation")
        rmtree("./Confusion_Matrix")
        rmtree("./Classifiers")

        # 4- Build new directory path!
        mkdir("Confusion_Matrix")
        mkdir("Cross_Validation")
        mkdir("Classifiers")


def check_files():
    if path.exists("./results.txt") and path.isfile("./results.txt"):
        return True

    if path.exists("./classification_reports.txt") and path.isfile("./classification_reports.txt"):
        return True

    if path.exists("./classification_reports.txt") and path.isfile("./classification_reports.txt"):
        return True

    if path.exists("./Cross_Validation") and path.isfile("./Cross_Validation"):
        return True

    if path.exists("./Confusion_Matrix") and path.isfile("./Confusion_Matrix"):
        return True

    if path.exists("./Classifiers") and path.isfile("./Classifiers"):
        return True
    return False
