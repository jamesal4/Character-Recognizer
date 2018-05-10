from csvImporting import allData, allLabels
import keras
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed
from keras.utils import to_categorical

# from sklearn.metrics import mean_squared_error


############# Helper functions
def unison_shuffle(a, b):
  assert len(a) == len(b)
  p = np.random.permutation(len(a))
  return a[p], b[p]


## Step 1 - Filter gyroscope/accelerometer data to include relevant datapoints
## Step 2 - run the examples through the network




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

x = np.array(x) # x.shape = (100, 1476)
y = np.array(y) # y.shape = (100, 2)
x = x.reshape(100, 1, 1476)

x, y = unison_shuffle(x, y)

## split data into train/test sets
numTrainExamples = int(.7*len(x))
trainX, trainY = x[:numTrainExamples], y[:numTrainExamples]
testX, testY = x[numTrainExamples:], y[numTrainExamples:]

numLSTMBlocks = 4

# 2c - create and fit lstm network
model = Sequential()
model.add(LSTM(numLSTMBlocks, input_shape=(1, maxLength*6)))
model.add(Dense(2))
model.compile(loss='mean_squared_error', optimizer='adam')
for i in range(100):
  model.fit(trainX, trainY, epochs=1, batch_size=10, verbose=2, shuffle=False)
  model.reset_states()

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# # invert predictions
# trainPredict = scaler.inverse_transform(trainPredict)
# trainY = scaler.inverse_transform([trainY])
# testPredict = scaler.inverse_transform(testPredict)
# testY = scaler.inverse_transform([testY])

# # calculate root mean squared error
# trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
# print('Test Score: %.2f RMSE' % (testScore))





