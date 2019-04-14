from misc import plot_grid_search
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron, PassiveAggressiveClassifier, SGDClassifier
import numpy as np


def tune_bayes(x, y, n_folds=10):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'alpha': c}
    model = MultinomialNB()
    true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    plot_grid_search(true_model.cv_results_, c, 'Multinomial_Bayes')
    return true_model


def tune_sgd(x, y, n_folds=10):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'alpha': c}
    model = SGDClassifier()
    true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    plot_grid_search(true_model.cv_results_, c, 'SGD_Classifier')
    return true_model


def tune_perceptron(x, y, n_folds=10):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'alpha': c}
    model = Perceptron()
    true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    plot_grid_search(true_model.cv_results_, c, "Perceptron")
    return true_model


def tune_passive_aggressive(x, y, n_folds=10):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'C': c}
    model = PassiveAggressiveClassifier(max_iter=1000)
    true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    plot_grid_search(true_model.cv_results_, c, 'Passive_Aggressive')
    return true_model
