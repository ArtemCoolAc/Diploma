#from prepare_avg_marks_datasets import merge_average_marks, fulfill_frame
from prepare_retakes_datasets import merge_retakes, fulfill_frame
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import numpy
import random

def student_retakes_learning_and_testing():
    groups = ['Б14-503', 'Б14-504', 'Б15-502', 'Б16-503', 'Б16-513']
    j1 = merge_retakes(groups)
    j2 = fulfill_frame(j1)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:5].T, dataset[5].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=random.randint(1,42)) 
    regr = MLPRegressor(random_state=1, max_iter=700, learning_rate_init=0.001,
     solver='sgd').fit(X_train, y_train)
    predicted = regr.predict(X_test)
    int_predicted = list(map(round, predicted))
    return predicted, y_test, int_predicted, regr.score(X_test, y_test)


if __name__ == '__main__':
    scores = []
    for i in range(20):
        predicted, y_test, int_predicted, score = student_retakes_learning_and_testing()
        scores.append(score)
    print(scores)