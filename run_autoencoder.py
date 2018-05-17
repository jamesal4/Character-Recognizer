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

def get_nearest_letter(letter_encodings, sample_encoding):
  nearest_letter = 0
  min_dist = float('inf')

  for letter in letter_encodings.keys():
    encoding = letter_encodings[letter]
    dist_to_encoding = np.linalg.norm(sample_encoding-encoding)

    if dist_to_encoding < min_dist:
      nearest_letter = letter
      min_dist = dist_to_encoding

  return nearest_letter

def get_overall_accuracy(letter_encodings, sample_encodings, labels):
  n_total = len(sample_encodings)
  n_correct = 0

  for ix, sample_encoding in enumerate(sample_encodings):
    nearest_letter = get_nearest_letter(letter_encodings, sample_encoding)
    if nearest_letter == labels[ix]:
      n_correct += 1

  return float(n_correct)/n_total

# how many relevant items are selected?
#   find nearest_letter for all encodings for given letter
#   (num A-examples correctly classified as "A")/(num examples listed as "A")
def get_recall(letter_encodings, sample_encodings, labels):
  letters = set(labels)

  recall = {}

  for letter in letters:
    letter_sample_encodings = sample_encodings[labels==letter]

    n_total = len(letter_sample_encodings)
    n_correct = 0

    for sample_encoding in letter_sample_encodings:
      nearest_letter = get_nearest_letter(letter_encodings, sample_encoding)
      if nearest_letter == letter:
        n_correct += 1

    recall[letter] = float(n_correct)/n_total

  return recall

# how many selected items are relevant?
#   find nearest_letter for all encodings
#   (num examples correctly classified as "A")/(num total examples classified as "A")
def get_precision(letter_encodings, sample_encodings, labels):
  letters = set(labels)

  precision = {}

  predictions = []
  for ix, sample_encoding in enumerate(sample_encodings):
    nearest_letter = get_nearest_letter(letter_encodings, sample_encoding)
    predictions.append(nearest_letter)
  predictions = np.array(predictions)

  for letter in letters:
    total_predictions_for_letter = len(np.where(predictions==letter)[0])
    total_correct_predictions_for_letter = 0

    for ix, label in enumerate(labels):
      if predictions[ix] == labels[ix] == letter:
        total_correct_predictions_for_letter += 1

    precision[letter] = float(total_correct_predictions_for_letter)/total_predictions_for_letter

  return precision

############# Helper functions


path_to_model = './models/autoencoder'
x = np.array([example.flatten() for example in allData])
x, y = unison_shuffle(x, stringLabels)

## Split into test/train
num_training_samples = int(.7*len(x))
x_train = x[:num_training_samples]
y_train = y[:num_training_samples]
x_test = x[num_training_samples:]
y_test = y[num_training_samples:]

train_autoencoder(x_train, x_test, path_to_model)


## Calculate encodings
model = keras.models.load_model(path_to_model+'.h5')
embedding_fn = keras.backend.function([model.layers[0].input], [model.layers[2].output])
all_sample_encodings = embedding_fn([x, 0])[0]
train_samples_encodings = embedding_fn([x_train, 0])[0]
test_sample_encodings = embedding_fn([x_test, 0])[0]
letter_encodings = compute_letter_encodings(train_samples_encodings, y_train)

## Calculate train/test accuracy
train_accuracy = get_overall_accuracy(letter_encodings, train_samples_encodings, y_train)
test_accuracy = get_overall_accuracy(letter_encodings, test_sample_encodings, y_test)

print ''
print 'train_accuracy', train_accuracy
print 'test_accuracy', test_accuracy
print ''

print 'letter-wise recall and precision'
recall = get_recall(letter_encodings, all_sample_encodings, y)
precision = get_precision(letter_encodings, all_sample_encodings, y)
for letter in set(y):
  print letter, round(recall[letter], 3), round(precision[letter], 3)

