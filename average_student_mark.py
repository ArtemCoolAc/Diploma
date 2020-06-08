from prepare_avg_marks_datasets import merge_average_marks, fulfill_frame
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import numpy
import random
from new_transform_from_EIS import all_groups
import csv


def average_student_mark_learning_and_testing(rs=7, outfile=None):
    groups = all_groups()
    j1 = merge_average_marks(groups)
    j2 = fulfill_frame(j1)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:5].T, dataset[5].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=rs)
    regr = MLPRegressor(random_state=1, max_iter=400, learning_rate_init=0.001,
    solver='sgd', hidden_layer_sizes=(40,)).fit(X_train, y_train)
    predicted = regr.predict(X_test)
    if outfile is not None:
        save_result_to_file(X_test, predicted, y_test, outfile, regr.score(X_test, y_test))
    return predicted, X_test, y_test, regr


def save_result_to_file(X_test, predicted, y_test, file_name, score):
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        diff = [(x, pred, y) for x, pred, y in 
        zip(X_test.tolist(), predicted.tolist(), y_test.tolist())]
        writer.writerow(['1T', '2T', '3T', '4T', '5T', 'predicted', '6Real'])
        for line in diff:
            writer.writerow([*line[0], line[1], line[2][0]])
        file.write(f'R^2 is {score}')


if __name__ == '__main__':
    scores = []
    a = [a for a in range(43)]
    for i in range(43):
        predicted, X_test, y_test, regr = average_student_mark_learning_and_testing(a[i])
        score = regr.score(X_test, y_test)
        scores.append(score)
    print(scores)
    print(sum(sorted(scores)[5:])/(len(scores)-5))