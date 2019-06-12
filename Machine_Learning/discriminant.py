from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
import time
from joblib import dump


def discriminant_line(train_x, train_y):
    lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
    start_time = time.time()
    lda.fit(train_x, train_y)
    print("--- Time to fit LDA: %s seconds ---" % (time.time() - start_time))
    print("Training Score (LDA): " + str(lda.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[LDA] Training Mean Test Score: " + str(lda.score(train_x, train_y)) + '\n')
    dump(lda, "./Classifiers/LDA.joblib")
    return lda


def discriminant_quad(train_x, train_y):
    qda = QuadraticDiscriminantAnalysis(store_covariance=False)
    start_time = time.time()
    qda.fit(train_x, train_y)
    print("--- Time to fit QDA: %s seconds ---" % (time.time() - start_time))
    print("Training Score is (QDA): " + str(qda.score(train_x, train_y)))

    with open("results.txt", "a+") as my_file:
        my_file.write("[QDA] Training Mean Test Score: " + str(qda.score(train_x, train_y)) + '\n')
    dump(qda, "./Classifiers/QDA.joblib")
    return qda
