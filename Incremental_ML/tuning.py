from misc import plot_grid_search
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron, PassiveAggressiveClassifier, SGDClassifier
from sklearn.linear_model import PassiveAggressiveRegressor, SGDRegressor
import numpy as np


def tune_bayes(x, y, n_folds=10, slow=True):
    print("Tuning Multinomial Bayes...")
    c = np.arange(0.01, 1.3, 0.01)
    param_grid = {'alpha': c}
    model = MultinomialNB()
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    true_model.fit(x, y)
    if slow:
        plot_grid_search(true_model.cv_results_, c, 'Multinomial_Bayes')
    print("Finished Tuning Multinomial Bayes...")
    return true_model


def tune_perceptron(x, y, n_folds=10, slow=True):
    print("Tuning Perceptron...")
    c = np.arange(0.01, 1.3, 0.01)
    param_grid = {'alpha': c}
    model = Perceptron(tol=1e-3, warm_start=True)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    true_model.fit(x, y)
    if slow:
        plot_grid_search(true_model.cv_results_, c, "Perceptron")
    print("Finished Tuning Perceptron...")
    return true_model


def tune_sgd_clf(x, y, n_folds=10, slow=True):
    print("Tuning SGD Classifier...")
    c = np.arange(0.0001, 0.01, 0.00001)
    param_grid = {'alpha': c}
    model = SGDClassifier(warm_start=True, tol=1e-3)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    true_model.fit(x, y)
    if slow:
        plot_grid_search(true_model.cv_results_, c, 'SGD_Classifier')
    print("Finished Tuning SGD Classifier...")
    return true_model


def tune_sgd_reg(x, y, n_folds=10, slow=True):
    print("Tuning SGD Regressor...")
    c = np.arange(0.0001, 0.01, 0.00001)
    param_grid = {'alpha': c}
    model = SGDRegressor(warm_start=True, tol=1e-3)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    true_model.fit(x, y)
    if slow:
        plot_grid_search(true_model.cv_results_, c, 'SGD_Regression')
    print("Finished Tuning SGD Regressor...")
    return true_model


def tune_passive_aggressive_clf(x, y, n_folds=10, slow=True):
    print("Tuning Passive Aggressive Classifier...")
    c = np.arange(0.01, 1.6, 0.01)
    param_grid = {'C': c}
    model = PassiveAggressiveClassifier(warm_start=True, tol=1e-3)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    true_model.fit(x, y)
    if slow:
        plot_grid_search(true_model.cv_results_, c, 'Passive_Aggressive_CLF')
    print("Finished Tuning Passive Aggressive Classifier...")
    return true_model


def tune_passive_aggressive_reg(x, y, n_folds=10, slow=True):
    print("Tuning Passive Aggressive Regression Classifier...")
    c = np.arange(0.01, 1.6, 0.01)
    param_grid = {'C': c}
    model = PassiveAggressiveRegressor(warm_start=True, tol=1e-3)
    if slow:
        true_model = GridSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    else:
        true_model = RandomizedSearchCV(model, param_grid, cv=n_folds, n_jobs=-1, error_score='raise', verbose=2)
    true_model.fit(x, y)
    if slow:
        plot_grid_search(true_model.cv_results_, c, 'Passive_Aggressive_Regression')
    print("Finished Tuning Passive Aggressive Regression...")
    return true_model
