import keras
import numpy as np

from csvImporting import allData, allLabels

from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten, Reshape
from keras.models import Model

def create_network(input_dim, loss):
  input_img = Input(shape=(input_dim,))

  # ## ENCODING
  # x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
  # x = MaxPooling2D((2, 2), padding='same')(x)
  # x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
  # x = MaxPooling2D((2, 2), padding='same')(x)
  # x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
  # x = MaxPooling2D((2, 2), padding='same')(x)
  # x = MaxPooling2D((2, 2), padding='same')(x) ## input is now 4x4x8

  # x = Flatten()(x)
  # x = Dense(32)(x)
  # x = Dense(128)(x)
  # x = Reshape((4, 4, 8))(x)

  # ## DECODING
  # x = UpSampling2D((2, 2))(x)
  # x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
  # x = UpSampling2D((2, 2))(x)
  # x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
  # x = UpSampling2D((2, 2))(x)
  # x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
  # x = UpSampling2D((2, 2))(x)
  # decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
  x = Dense(64, activation='relu')(input_img)
  x = Dense(16, activation='relu')(x)
  x = Dense(64, activation='relu')(x)
  decoded = Dense(input_dim, activation='sigmoid')(x)

  autoencoder = Model(input_img, decoded)
  autoencoder.compile(optimizer='adadelta', loss=loss)
  return autoencoder

def main():

  x = np.array([example.flatten() for example in allData])

  input_dim = x.shape[1]

  x_train = x[:int(.7*len(x))]
  x_test = x[int(.7*len(x)):]

  # loss = 'mae'
  loss = 'binary_crossentropy'
  model = create_network(input_dim, loss)
  model.summary()
  model.fit(x_train, x_train, epochs=150, shuffle=True, validation_data=(x_test, x_test))
  model.save('./models/ae.h5')

if __name__ == '__main__':
    main()
