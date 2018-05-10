from csvImporting import allData, allLabels
import keras
import math
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed
from keras.utils import to_categorical

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


############# Helper functions
def unison_shuffle(a, b):
  assert len(a) == len(b)
  p = np.random.permutation(len(a))
  return a[p], b[p]

def dot_product(v1, v2):
  return v1[0]*v2[0] + v1[1]*v2[1]

def calculate_accuracy(predictions, actual):
  assert len(predictions) == len(actual)

  numTotalPredictions = len(predictions)
  numCorrectPredictions = 0
  for ix in range(numTotalPredictions):
    if round(dot_product(predictions[ix], actual[ix])) == 1.0:
      numCorrectPredictions += 1

  return float(numCorrectPredictions)/numTotalPredictions

def calculate_mse(predictions, actual):
  pass

############# Helper functions


## TODO:
# - rescale inputs (MaxMinScaler)
# - filter the gyroscope/accelerometer data to include only relevant datapoints


## pad examples so that they are of equal length
x = []
y = []
maxLength = max([len(ex) for ex in allData])

for ix, example in enumerate(allData):
  example_row = []
  for val in example:
    example_row.extend(val)

  pad_length = (maxLength - len(example))*6
  example_row.extend([0.]*pad_length)

  x.append(np.array(example_row))
  y.append(np.array(allLabels[ix]))

print(x[0])

x = np.array(x) # x.shape = (100, 1476)
y = np.array(y) # y.shape = (100, 2)
x = x.reshape(100, 1, 1476)
y = y.reshape(100, 2)

x, y = unison_shuffle(x, y)

## split data into train/test sets
numTrainExamples = int(.7*len(x))
trainX, trainY = x[:numTrainExamples], y[:numTrainExamples]
testX, testY = x[numTrainExamples:], y[numTrainExamples:]

numLSTMBlocks = 9

# 2c - create and fit lstm network
model = Sequential()
model.add(LSTM(numLSTMBlocks, input_shape=(1, maxLength*6)))
model.add(Dense(2))
model.compile(loss='mean_squared_error', optimizer='adam')
for i in range(1):
  model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2, shuffle=False)
  model.reset_states()

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

training_accuracy = calculate_accuracy(trainPredict, trainY)
test_accuracy = calculate_accuracy(testPredict, testY)

print('training accuracy: ' + str(training_accuracy))
print('test accuracy: ' + str(test_accuracy))
