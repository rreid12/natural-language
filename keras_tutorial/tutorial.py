from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.losses import categorical_crossentropy
import numpy as np

'''
Keras Sequential Model Tutorial Example - Binary classification
	-uses tensorflow as backend
	
https://keras.io/getting-started/sequential-model-guide/
'''

#Create a seuential modelers
model = Sequential()

#add two layers
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dense(1, activation='sigmoid'))

#Binary classification compilation (as I understand this, it means classify something as one thing or another)
model.compile(optimizer='rmsprop',
	loss='binary_crossentropy',
	metrics=['accuracy'])

#Generate dummy data
data = np.random.random((1000, 100))
labels = np.random.randint(2, size=(1000, 1))

#Train model, iterating on the data in batches of 32 samples
model.fit(data, labels, epochs=10, batch_size=32)