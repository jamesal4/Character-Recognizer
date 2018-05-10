from csvImporting import allData, allLabels
import keras
import numpy as np

### Step 1 - Filter gyroscope/accelerometer data to include relevant datapoints

### Step 2 - run the examples through the network


from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed
from keras.utils import to_categorical
import numpy as np



print allData.shape
print allLabels.shape



# model = Sequential()

# model.add(LSTM(32, return_sequences=True, input_shape=(None, 1)))
# model.add(LSTM(8, return_sequences=True))
# model.add(TimeDistributed(Dense(2, activation='sigmoid')))

# print(model.summary(90))

# model.compile(loss='categorical_crossentropy',
#               optimizer='adam')

# model.fit(x=allData, y=allLabels, batch_size=None, epochs=10, steps_per_epoch=10, verbose=1)
