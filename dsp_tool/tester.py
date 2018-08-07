#!/usr/bin/pickle
'''
-This testing script was originally designed for an Udacity course's final project:
https://classroom.udacity.com/courses/ud120
-Essentially acts as a wrapper for scikit-learn's StratifiedShuffleSplit
-Adapting it now for testing our 'ily' vs 'ihy' classifiers
'''

import pickle
import sys
from sklearn.cross_validation import StratifiedShuffleSplit
from feature_format import featureFormat, targetFeatureSplit

#Formatted string for output
PERF_FORMAT_STRING = "\
\tAccuracy: {:>0.{display_precision}f}\t\tPrecision: {:>0.{display_precision}f}\t\
Recall: {:>0.{display_precision}f}\t\tF1: {:>0.{display_precision}f}\t\tF2: {:>0.{display_precision}f}"
RESULTS_FORMAT_STRING = "\tTotal predictions: {:4d}\tTrue positives: {:4d}\tFalse positives: {:4d}\
\tFalse negatives: {:4d}\tTrue negatives: {:4d}"

TRI_FORMAT_STRING = "\
\tAccuracy: {:>0.{display_precision}f}\tPrecision: {:>0.{display_precision}f}\t\
Recall: {:>0.{display_precision}f}"

'''
Cross validate a given classifier using StratifiedShuffleSplit
http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html

Folds refer to splits of the data
    -so the model will be trained using 1000 different splits of the training and testing data
    -this can provide much more valuable insight into the performance of the given classifier

Essentially an evaluation tool
'''
def test_binary_classifier(clf, dataset, feature_list, folds = 1000):
    #format the data into its features and labels
    data = featureFormat(dataset, feature_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    #create the stratified shuffle split cross-validator
    cv = StratifiedShuffleSplit(labels, folds, random_state = 42)

    #initialize metrics
    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0

    #add features and labels to lists
    for train_idx, test_idx in cv: 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
        
        ### fit the classifier using training set, and test on test set
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
                #next...

            else:
                print "Warning: Found a predicted label not == 0 or 1."
                print "All predictions should take value 0 or 1."
                print "Evaluating performance for processed predictions:"
                break

    #calculate various other metrics that help to evaluate the model, print resutls            
    try:
        total_predictions = true_negatives + false_negatives + false_positives + true_positives
        accuracy = 1.0*(true_positives + true_negatives)/total_predictions
        precision = 1.0*true_positives/(true_positives+false_positives)
        recall = 1.0*true_positives/(true_positives+false_negatives)
        f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
        f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
        print clf
        print PERF_FORMAT_STRING.format(accuracy, precision, recall, f1, f2, display_precision = 5)
        print RESULTS_FORMAT_STRING.format(total_predictions, true_positives, false_positives, false_negatives, true_negatives)
        print ""
    except:
        print "Got a divide by zero when trying out:", clf
        print "Precision or recall may be undefined due to a lack of true positive predicitons."

def test_tri_classifier(clf, dataset, feature_list, folds=1000):
    #format the data into its features and labels
    data = featureFormat(dataset, feature_list, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    #create the stratified shuffle split cross-validator
    cv = StratifiedShuffleSplit(labels, folds, random_state = 42)

    #initialize metrics
    confusion_matrix = {0: [0, 0, 0], 1: [0, 0, 0], 2: [0, 0, 0]}

    #add features and labels to lists
    for train_idx, test_idx in cv: 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
        
        ### fit the classifier using training set, and test on test set
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)

        for prediction, truth in zip(predictions, labels_test):
            confusion_matrix[int(prediction)][int(truth)] += 1

    
    print(confusion_matrix)

    
    total_predictions = sum(confusion_matrix[0]) + sum(confusion_matrix[1]) + sum(confusion_matrix[2])
    accuracy = 1.0*(confusion_matrix[0][0] + confusion_matrix[1][1] + confusion_matrix[2][2]) / total_predictions

    print('total predictions/accuracy:\nPREDICTIONS: {pred}\nOVERALL_ACCURACY: {acc}'.format(pred=total_predictions, acc=accuracy))
    print('\nmetrics for ihy:')
    calculte_evaluation_metrics(confusion_matrix, 0)
    print('\nmetrics for ily:')
    calculte_evaluation_metrics(confusion_matrix, 1)
    print('\nmetrics for iky:')
    calculte_evaluation_metrics(confusion_matrix, 2)


def calculte_evaluation_metrics(conf_matrix, row):
    true_positives = conf_matrix[row][row]

    #tn
    true_negatives = 0
    for rw in conf_matrix:
        if conf_matrix[rw] != conf_matrix[row]:
            true_negatives += conf_matrix[rw][rw]


    false_positives = 0

    for elm in conf_matrix[row]:
        if elm is not conf_matrix[row][row]:
            false_positives += elm


    false_negatives = 0

    for i in range(0,len(conf_matrix)):
        if i is not row:
            false_negatives += conf_matrix[i][row]

    try:
        total_predictions = true_negatives + false_negatives + false_positives + true_positives
        accuracy = 1.0*(true_positives + true_negatives)/total_predictions
        precision = 1.0*true_positives/(true_positives+false_positives)
        recall = 1.0*true_positives/(true_positives+false_negatives)
        f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
        f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
        #print clf
        print PERF_FORMAT_STRING.format(accuracy, precision, recall, f1, f2, display_precision = 5)
        print RESULTS_FORMAT_STRING.format(total_predictions, true_positives, false_positives, false_negatives, true_negatives)
        print ""
    except:
        print "Got a divide by zero when trying out."
        print "Precision or recall may be undefined due to a lack of true positive predicitons."
