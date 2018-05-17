import keras
import numpy as np

from autoencoder import train_autoencoder
from csvImporting import allData, allLabels, stringLabels


############# Helper functions
def unison_shuffle(a, b):
  assert len(a) == len(b)
  p = np.random.permutation(len(a))
  return a[p], b[p]

def compute_letter_encodings(train_samples_encodings, y_train):
  assert train_samples_encodings.shape[0] == y_train.shape[0]

  encodings = {}

  all_letters = set(y_train)
  for letter in all_letters:
    letter_encodings = train_samples_encodings[y_train==letter]
    letter_encoding = np.mean(letter_encodings, axis=0)
    encodings[letter] = letter_encoding

  return encodings

def get_nearest_ltter(letter_encodings, sample_encoding):
  nearest_letter = 0
  min_dist = float('inf')

  for letter in letter_encodings.keys():
    encoding = letter_encodings[letter]
    dist_to_encoding = np.linalg.norm(sample_encoding-encoding)

    if dist_to_encoding < min_dist:
      nearest_letter = letter
      min_dist = dist_to_encoding

  return nearest_letter

def get_accuracy(letter_encodings, sample_encodings, labels):
  n_total = len(sample_encodings)
  n_correct = 0

  for ix, sample_encoding in enumerate(sample_encodings):
    nearest_letter = get_nearest_ltter(letter_encodings, sample_encoding)
    if nearest_letter == labels[ix]:
      n_correct += 1

  return float(n_correct)/n_total

############# Helper functions


path_to_model = './models/ae.h5'
x = np.array([example.flatten() for example in allData])
x, y = unison_shuffle(x, stringLabels)

## Split into test/train
num_training_samples = int(.7*len(x))
x_train = x[:num_training_samples]
y_train = y[:num_training_samples]
x_test = x[num_training_samples:]
y_test = y[num_training_samples:]

train_autoencoder(x_train, x_test, path_to_model)

# 1. Compute each example's sample-encoding
# 2. Compute letter-encoding - average sample-encoding for all examples for given letter
# 3. Calculate training-accuracy
# 4. Calculate test-accuracy

## Calculate encodings
model = keras.models.load_model(path_to_model)
embedding_fn = keras.backend.function([model.layers[0].input], [model.layers[2].output])
train_samples_encodings = embedding_fn([x_train, 0])[0]
test_sample_encodings = embedding_fn([x_test, 0])[0]
letter_encodings = compute_letter_encodings(train_samples_encodings, y_train)

train_accuracy = get_accuracy(letter_encodings, train_samples_encodings, y_train)
test_accuracy = get_accuracy(letter_encodings, test_sample_encodings, y_test)

print 'train_accuracy', train_accuracy
print 'test_accuracy', test_accuracy


