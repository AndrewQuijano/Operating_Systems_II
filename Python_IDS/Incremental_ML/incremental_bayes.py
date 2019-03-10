from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import brier_score_loss


def build_bayes(x_train, y_train, x_test=None, y_test=None):
    # Gaussian Naive-Bayes with no calibration
    clf = MultinomialNB(class_prior=None, fit_prior=True)
    clf.partial_fit(x_train, y_train)
    return clf

