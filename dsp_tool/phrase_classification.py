import numpy as np 
import scipy.io
import os
import json
import time
import sys

from matlab_client import MatlabClient

import matplotlib.pyplot as plt

from feature_format import featureFormat, targetFeatureSplit
from tester import test_tri_classifier

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline


'''
Plots two features against each other in a scatter plot and displays the result
	-x_data: data plotted on x-axis
	-y_data: data plotted on y-axis
'''
def draw_scatter_plot(x_data, y_data):
	features = ['id', x_data, y_data]

	#convert data into formatted features
	data = featureFormat(data_dict, features)

	#plot all data points on the graph
	for point in data:
		x = point[1]
		y = point[2]
		if point[0] == 1:
			plt.scatter(x, y, color='r') #color 'ily' phrases red
		elif point[0] == 0:
			plt.scatter(x, y, color='#000000') #color 'ihy' phrases black
		elif point[0] == 2:
			plt.scatter(x, y, color='g')

	#set up and display the plot
	plt.xlabel(x_data)
	plt.ylabel(y_data)
	plt.show()

def predict_unseen_wav_file():
	'''TODO: function make a prediction based on a single unseen .wav file'''
	pass

'''
Uses GridSearchCV to search through a given list of paramters for the classifier and returns the 
best best_estimator_ of the classifiers tested
	-name: name of the classifier type
	-clf: pass in the classifier object
	-paramters: dict of all testing paramters
'''
def search_classifier_parameters(name, clf, parameters):

	#split features/labels into training and testing sets
	features_train, features_test, labels_train, labels_test = \
    	train_test_split(features, labels, test_size=0.2, random_state=42) 

    #can use a selectKBest method for feature selection (in this case, just use all)
	kbest = SelectKBest(k='all')
	scaler = MinMaxScaler()

	#create a pipeline and fit it so that features can be selected, scaled, etc. in a smooth step
	pipeline = Pipeline(steps=[('min_max_scaler', scaler), ('feature_selection', kbest), (name, clf)])
	pipeline.fit(features_train, labels_train)

	'''create the GridSearchCV, fit it using all possible combinations of the given parameters, and return the object
	so that the best_estimator_ attribute can be used
	'''
	cv = GridSearchCV(pipeline, param_grid=parameters, scoring='accuracy', cv=5)
	t0 = time.time() #keep track of time it takes to fit all combinations of parameters
	cv.fit(features_train, labels_train)
	print('Time spent assessing classifer options: {t}s'.format(t=time.time() - t0)) #print time spent fitting to the screen
	print('Best parameters: {param}'.format(param=cv.best_params_)) #show best parameters
	score = cv.score(features_test, labels_test)
	print('{classifier} score: {scr}'.format(classifier=name, scr=cv.best_score_)) #show the score


	return cv


if __name__ == '__main__':
	'''
	-Use matlab API to run all recordings through the DSP tool (AudioTimeFilter)
	-Define classifiers and their paramters that can be trained/tested
	-Using all combinations of paramters, use GridSearchCV wrapper method (aka: search_classifier_parameters()) to
	train all possible combinations of the model
	-Test the best_estimator_ (from the GridSearchCV) of each classifier type exhaustively using the tester.py script
		-this will display the accuracy, precision, recall, f1-score, f2-score, true-positives, false-positives, true-negatives,
		false-negatives, total predictions, etc. to the screen

	TODO: 
		-seperate the matlab execution from the training/selection of the ML models
		-define constants properly
		-find/create more features to use
		-test more classifier types?

	'''

	if len(sys.argv) > 1:
		if sys.argv[1] == '-matlab':
			client = MatlabClient(['recordings/ily_combo', 'recordings/ihy_combo', 'recordings/iky'],
				['keypressTimeLog', 'wordTimeArray'])

	data_dict = {}

	'''
	- runs each .wav file through the MATLAB script, which updates the to_language_model.mat file with the .wav file's timing data_dict
	- that data is then loaded into python and stored in a dict (data_dict)
		- filename is the key, all the features are the values
	-file structure must be consistent for this project:

		- root_dir:
			- phrase_classification.py
			- AudioTimeFilter.m
			- tester.py
			- to_language_model.mat
			- recordings
				- ily_combo
					- .wav files for classification
				- ihy_combo
					- .wav files for classification
				- iky
					- .wav files for classification
			- .data_to_lm
				- ily
					- .mat files
				- ihy
					- .mat files
				- iky
					- .mat files
	'''

	'''
	directories of interest (ex: 'ily' and 'ihy')

	for d in directories:
		if file ends with .mat:
			filename = os.path.join('.data_to_lm', d, file)

			loader = scipy.io.loadmat(filename)
			data_dict[filename][id] = phrases[d]

			

	'''

	directories = ['ihy', 'ily', 'iky']

	for directory in os.listdir('.data_to_lm'):
		#print('directory: {d}'.format(d=directory))
		sub_directory = os.path.join('.data_to_lm', directory)
		#print('sub_directory: {s}'.format(s=sub_directory))
		if directory in directories:
			for file in os.listdir(sub_directory):
				if file.endswith('.mat'):
					filename = os.path.join(sub_directory, file)

					loader = scipy.io.loadmat(filename)
					data_dict[filename] = {}

					if directory in filename:
						data_dict[filename]['id'] = directories.index(directory)
					else:
						continue

					data_dict[filename]['avg_time_between_keypress'] = np.average(loader['keypressTimeLog'])
					data_dict[filename]['avg_word_typing_time'] = np.average(loader['wordTimeArray'])
					data_dict[filename]['phrase_typing_time'] = np.sum(loader['wordTimeArray'])
					data_dict[filename]['spc_keypress'] = loader['keypressTimeLog'][1] #spc - l / spc - h
					data_dict[filename]['lttr_keypress1'] = loader['keypressTimeLog'][2] #l - o / h - a
					data_dict[filename]['lttr_keypress2'] = loader['keypressTimeLog'][3] #o - v / a - t
					data_dict[filename]['lttr_keypress3'] = loader['keypressTimeLog'][4] #v - e / t - e


	'''
	for file in os.listdir('.data_to_lm'):
		if file.endswith('.mat'):
			filename = os.path.join('.data_to_lm', file)

			loader = scipy.io.loadmat(filename)
			data_dict[filename] = {}


			if 'ily' in filename:
				data_dict[filename]['isLove'] = True
			elif 'ihy' in filename:
				data_dict[filename]['isLove'] = False
			else:
				raise EnvironmentError('File found that does not match any given label!')

			data_dict[filename]['avg_time_between_keypress'] = np.average(loader['keypressTimeLog'])
			data_dict[filename]['avg_word_typing_time'] = np.average(loader['wordTimeArray'])
			data_dict[filename]['phrase_typing_time'] = np.sum(loader['wordTimeArray'])
			data_dict[filename]['spc_keypress'] = loader['keypressTimeLog'][1] #spc - l / spc - h
			data_dict[filename]['lttr_keypress1'] = loader['keypressTimeLog'][2] #l - o / h - a
			data_dict[filename]['lttr_keypress2'] = loader['keypressTimeLog'][3] #o - v / a - t
			data_dict[filename]['lttr_keypress3'] = loader['keypressTimeLog'][4] #v - e / t - e
	'''


	features_list = ['id', 'avg_time_between_keypress', 'avg_word_typing_time', 'phrase_typing_time', 'spc_keypress', 'lttr_keypress1', 'lttr_keypress2', 'lttr_keypress3']

	my_dataset = data_dict

	#transform the data into features and labels so that they can be used in scikit-learn
	data = featureFormat(my_dataset, features_list, sort_keys=True)
	labels, features = targetFeatureSplit(data)

	draw_scatter_plot('phrase_typing_time', 'spc_keypress') #example of how to use draw_scatter_plot()


	#classifiers to be trained/tested/evaluated
	classifiers = ['logistic_reg', 'decision_tree', 'svm', 'random_forest']


	for clf_type in classifiers:
		if clf_type == 'decision_tree':
			#sets up parameters for each different classifier
			parameters = dict(decision_tree__min_samples_leaf=range(1,5),
				decision_tree__max_depth=range(1,5),
				decision_tree__class_weight=['balanced'],
				decision_tree__criterion=['gini', 'entropy'])

			#create the classifier, find the classifiers best parameters, and test the best version of that classifier
			clf = DecisionTreeClassifier()
			clf = search_classifier_parameters(clf_type, clf, parameters)
			test_tri_classifier(clf.best_estimator_, my_dataset, features_list)


		elif clf_type == 'logistic_reg':
			parameters = dict(logistic_reg__class_weight=['balanced'],
		    	logistic_reg__solver=['liblinear'],
		    	logistic_reg__C=[0.1, 0.2, 0.3, 0.5, 1.0],
				logistic_reg__random_state=[42])

			clf = LogisticRegression()
			clf = search_classifier_parameters(clf_type, clf, parameters)
			test_tri_classifier(clf.best_estimator_, my_dataset, features_list)

		elif clf_type == 'svm':
			parameters = dict(svm__kernel=['rbf', 'linear'],
				svm__C=[1.0, 10.0, 100.0, 1000.0, 10000.0],
				svm__class_weight=['balanced'])

			clf = SVC()
			clf = search_classifier_parameters(clf_type, clf, parameters)
			test_tri_classifier(clf.best_estimator_, my_dataset, features_list)


		elif clf_type == 'random_forest':
			parameters = dict(random_forest__n_estimators=range(5,10),
				random_forest__min_samples_leaf=range(1,5),
				random_forest__max_depth=range(1,5))
			#maximize recall??

			clf = RandomForestClassifier()
			clf = search_classifier_parameters(clf_type, clf, parameters)
			test_tri_classifier(clf.best_estimator_, my_dataset, features_list)


		else:
			print('Invalid classifier found. Exiting.')
			sys.exit()




'''
hate: 0
love: 1

{
	ily1.wav: {
		phrase_typing_time:
		typing_time_per_word:
		avg_time_between_keypress:
		keypress_timelog:
		isLove:
		spc_to_l/h:????
	}
}
'''