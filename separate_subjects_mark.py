from prepare_sep_subjects_datasets import merge_english_marks, fulfill_frame
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy
import random
from new_transform_from_EIS import all_groups
import csv


def separate_subjects_mark_lerning_and_testing(rs=36, outfile=None):
    groups = all_groups()
    j1 = merge_english_marks(groups)
    j2 = fulfill_frame(j1, 0, 4)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:-1].T, dataset[-1].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=rs)
    classifier = MLPClassifier(random_state=1, max_iter=5000, learning_rate_init=0.001,
     solver='lbfgs', hidden_layer_sizes=(10,)).fit(X_train, y_train)
    predicted = classifier.predict(X_test)
    if outfile is not None:
        save_result_to_file(X_test, predicted, y_test,
         outfile, classifier.score(X_test, y_test))
    return predicted, X_test, y_test, classifier


def save_result_to_file(X_test, predicted, y_test, file_name, score):
    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        diff = [(x, pred, y) for x, pred, y in 
        zip(X_test.tolist(), predicted.tolist(), y_test.tolist())]
        writer.writerow(['1T', '2T', '3T', 'predicted', '4Real'])
        for line in diff:
            writer.writerow([*line[0], line[1], line[2][0]])
        writer.writerow(f'Accuracy is {score}') 


if __name__ == '__main__':
    scores = []
    a = [a for a in range(43)]
    for i in range(43):
        predicted, X_test, y_test, classifier = separate_subjects_mark_lerning_and_testing(a[i])
        scores.append(classifier.score(X_test, y_test))
    print(scores)
    print(sum(sorted(scores)[5:])/(len(scores)-5))
    