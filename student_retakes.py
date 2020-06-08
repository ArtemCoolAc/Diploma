#from prepare_avg_marks_datasets import merge_average_marks, fulfill_frame
from prepare_retakes_datasets import merge_retakes, fulfill_frame
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import numpy
import random
from new_transform_from_EIS import all_groups
from average_student_mark import save_result_to_file


def student_retakes_learning_and_testing(rs=3, outfile=None):
    groups = all_groups()
    j1 = merge_retakes(groups)
    j2 = fulfill_frame(j1)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:5].T, dataset[5].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=rs) 
    regr = MLPRegressor(random_state=1, max_iter=700, learning_rate_init=0.001,
     solver='sgd').fit(X_train, y_train)
    predicted = regr.predict(X_test)
    int_predicted = list(map(round, predicted))
    if outfile is not None:
        save_result_to_file(X_test, predicted, y_test, outfile, regr.score())
    return predicted, int_predicted, X_test, y_test, regr


if __name__ == '__main__':
    scores = []
    a = [b for b in range(43)]
    for i in range(43):
        int_predicted, predicted, x_test, y_test,  regr = student_retakes_learning_and_testing(a[i])
        scores.append(regr.score(x_test, y_test))
    print(scores)
    print(sum(sorted(scores)[5:])/(len(scores)-5))