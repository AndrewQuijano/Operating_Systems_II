from misc import plot_grid_search
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron, PassiveAggressiveClassifier, SGDClassifier
from sklearn.linear_model import PassiveAggressiveRegressor, SGDRegressor
import numpy as np


def tune_bayes(x, y, n_folds=10, slow=True):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'alpha': c}
    model = MultinomialNB()
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
        plot_grid_search(true_model.cv_results_, c, 'Multinomial_Bayes')
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    return true_model


def tune_perceptron(x, y, n_folds=10, slow=True):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'alpha': c}
    model = Perceptron(warm_start=True)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
        plot_grid_search(true_model.cv_results_, c, "Perceptron")
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    return true_model


def tune_sgd_clf(x, y, n_folds=10, slow=True):
    c = np.arange(0.0001, 0.01, 0.01)
    param_grid = {'alpha': c}
    model = SGDClassifier(warm_start=True, max_iter=10)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
        plot_grid_search(true_model.cv_results_, c, 'SGD_Classifier')
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    return true_model


def tune_passive_aggressive_clf(x, y, n_folds=10, slow=True):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'C': c}
    model = PassiveAggressiveClassifier(warm_start=True, max_iter=10)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
        plot_grid_search(true_model.cv_results_, c, 'Passive_Aggressive_CLF')
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    return true_model


def tune_sgd_reg(x, y, n_folds=10, slow=True):
    c = np.arange(0.0001, 0.01, 0.01)
    param_grid = {'alpha': c}
    model = SGDRegressor(warm_start=True, max_iter=10)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
        plot_grid_search(true_model.cv_results_, c, 'SGD_Regression')
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    return true_model


def tune_passive_aggressive_reg(x, y, n_folds=10, slow=True):
    c = np.arange(0.01, 1, 0.01)
    param_grid = {'C': c}
    model = PassiveAggressiveRegressor(warm_start=True, max_iter=10)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
        plot_grid_search(true_model.cv_results_, c, 'Passive_Aggressive_Regression')
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise')
    true_model.fit(x, y)
    return true_model
