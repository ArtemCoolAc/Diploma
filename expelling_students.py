from prepare_expel_dataset import merge_preliminary_data, correct_dataset
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.model_selection import train_test_split, cross_val_score
import numpy
import random
import graphviz
from new_transform_from_EIS import all_groups
import os


def expelling_students_create_and_learn():
    # groups = ['Б14-503', 'Б14-504', 'Б15-502', 'Б16-503', 'Б16-513']
    groups = all_groups()
    j1 = merge_preliminary_data(groups)
    j2 = correct_dataset(j1)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:4].T, dataset[4].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=random.randint(1,42))
    classifier = MLPClassifier(random_state=1, max_iter=5000, learning_rate_init=0.001,
     solver='sgd', hidden_layer_sizes=(10,)).fit(X_train, y_train)

    # R^2 ~ 0.77 hls=10 
    predicted = classifier.predict(X_test)
    return predicted, y_test, classifier.score(X_test, y_test)


def expelling_students_tree_learn(maximum_depth=None):
    groups = all_groups()
    j1 = merge_preliminary_data(groups)
    j2 = correct_dataset(j1)
    dataset = numpy.matrix([elem for elem in j2.values()])
    dataset = dataset.T
    x,y = dataset[:4].T, dataset[4].T
    X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=random.randint(1,42))
    tree = DecisionTreeClassifier(max_depth=maximum_depth).fit(X_train, y_train)
    predicted = tree.predict(X_test)
    return predicted, X_test, y_test, tree
    #score = cross_val_score(tree, x,y, cv=23)
    #print(score.mean(), score.std())
    #X_train, X_test, y_train, y_test = train_test_split(x,y, random_state=random.randint(1,42))
    #print(score)


def visualize_decision_tree(max_depth=3):
    name = 'Wounderful_tree.dot' if max_depth == 3 else 'Depth_tree.dot'
    predicted, X_test, y_test, tree = expelling_students_tree_learn(maximum_depth=max_depth)
    dot_data = export_graphviz(tree, out_file=None, 
        feature_names=['pretest', 'exam', 'mean_mark', 'extra_terms'], filled=True,
        rounded=True, special_characters=True, class_names=['False', 'True']) 
    graph = graphviz.Source(dot_data)
    graph.save(name)
    os.system(f'dot -Tpng {name} -o {name[:-4]}.png')
    return tree.score(X_test, y_test)


if __name__ == '__main__':
    scores = []
    for i in range(50):
        predicted, X_test, y_test, tree = expelling_students_tree_learn()
        scores.append(tree.score(X_test, y_test))
    print(scores)
    print(sum(sorted(scores)[5:])/(len(scores)-5))
