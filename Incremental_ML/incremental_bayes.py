from sklearn.naive_bayes import MultinomialNB


def build_bayes(x_train, y_train):
    # Gaussian Naive-Bayes with no calibration
    clf = MultinomialNB(class_prior=None, fit_prior=True)
    clf.partial_fit(x_train, y_train)
    return clf

