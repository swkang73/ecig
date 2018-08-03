'''Ecig Random Forest Classifier
classifies e-cigarette mass scan into three e-cig (G6 / Juul / Blu)
reference 1: https://chrisalbon.com/machine_learning/trees_and_forests/random_forest_classifier_example/
reference 2: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
'''

import os, csv, numpy as np, matplotlib.pyplot as plt, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz

RANDOM_STATE = 0
CIGTOTAL = 4
G6 = 1
JUUL = 2
BLU = 3
V2 = 4

print('Read training data...')
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

print('RF Training...')
train_label = np.array(train_label)
train_data = np.array(train_data)
clf = RandomForestClassifier(max_features='sqrt', n_jobs=2, random_state=RANDOM_STATE)
clf.fit(train_data, train_label)


print('Read testing data...')
with open('testing.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = np.array(test_data)
decision_path = clf.decision_path(test_data)
feature_label = []
for i in range(3088):
    feature_label.append(str(i))


# understand tree structure
# ref 1: http://scikit-learn.org/stable/auto_examples/tree/plot_unveil_tree_structure.html
# ref 2: https://stackoverflow.com/questions/40155128/plot-trees-for-a-random-forest-in-python-with-scikit-learn
# parse tree structure and save the info by txt, png, and dot 

f = open('rf_tree_explanation.txt', 'a')
for treeIndex in range(len(clf.estimators_)):
    f.write('Tree number %d\n' % (treeIndex + 1))
    n_nodes = clf.estimators_[treeIndex].tree_.node_count
    children_left = clf.estimators_[treeIndex].tree_.children_left
    children_right = clf.estimators_[treeIndex].tree_.children_right
    feature = clf.estimators_[treeIndex].tree_.feature
    threshold = clf.estimators_[treeIndex].tree_.threshold

    # The tree structure can be traversed to compute various properties such
    # as the depth of each node and whether or not it is a leaf.
    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1

        # If we have a test node
        if (children_left[node_id] != children_right[node_id]):
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True

    f.write("The binary tree structure has %s nodes and has "
          "the following tree structure:\n"
          % n_nodes)

    for i in range(n_nodes):
        if is_leaves[i]:
            f.write("%snode=%s leaf node.\n" % (node_depth[i] * "\t", i))
        else:
            f.write("%snode=%s test node: go to node %s if measurement as m/z of %s <= %s else to "
                  "node %s.\n"
                  % (node_depth[i] * "\t",
                     i,
                     children_left[i],
                     feature[i],
                     threshold[i],
                     children_right[i],
                     ))

    f.write('\n \n')
    export_graphviz(clf.estimators_[treeIndex],
                    feature_names=feature_label,
                    filled=True,
                    out_file='tree_%d.dot' % (treeIndex + 1) )
    os.system('dot -Tpng tree_%d.dot -o tree_%d.png' % (treeIndex + 1, treeIndex + 1))

f.close()

# see each feature importance
index, count = (0 for i in range(2))
for imp in clf.feature_importances_:
    if imp != 0.:
        count += 1
        print('m/z: %d importance: %.4f' % (index, imp))
    index += 1
print('total number of features: %d' % count)


