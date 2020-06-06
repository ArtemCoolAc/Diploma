from prepare_sep_subjects_datasets import merge_english_marks, fulfill_frame
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy
import random


def separate_subjects_mark_lerning_and_testing():
    groups = ['Б14-503', 'Б14-504', 'Б15-502', 'Б16-503', 'Б16-513']
    j1 = merge_english_marks(groups)
    j2 = fulfill_frame(j1, 0)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:5].T, dataset[5].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=random.randint(1,42))
    classifier = MLPClassifier(random_state=1, max_iter=5000, learning_rate_init=0.001,
     solver='sgd', hidden_layer_sizes=(10,)).fit(X_train, y_train)
    # R^2 ~ 0.4, hls=10
    # classifier = MLPClassifier(random_state=1, max_iter=5000, learning_rate_init=0.001,
    # solver='sgd').fit(X_train, y_train)
    # R^2 ~ 0.39 hls = (100,), lr=0.001
    predicted = classifier.predict(X_test)
    return predicted, y_test, classifier.score(X_test, y_test)

if __name__ == '__main__':
    scores = []
    for i in range(50):
        predicted, y_test, score = separate_subjects_mark_lerning_and_testing()
        scores.append(score)
    print(scores)
    print(sum(sorted(scores)[5:])/(len(scores)-5))
    