import pickle
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

with open('./dataset/image_list_blue_learning.txt', 'rb') as img:
    image = pickle.load(img, encoding='latin1')

with open('./dataset/angle_list_blue_learning.txt', 'rb') as agl:
    angle = pickle.load(agl, encoding='latin1')

#threshold
THRESHOLD = 225
image = np.where(image < THRESHOLD, 0, 1)

#shuffle
image = image.reshape(len(angle), -1)
p = np.random.permutation(len(angle))
image = image[p]
angle = angle[p]
#make train_data and test_data
image_train = image[:5500]
angle_train = angle[:5500]
image_test = image[5500:]
angle_test = angle[5500:]
#angle_test = angle_test.reshape(-1, 1)


def build_model():
    model = keras.Sequential([
        layers.Dense(100, activation='relu', input_shape=[len(image_train[0])]),
        layers.Dense(200, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.01)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae', 'mse'])
    return model

model = build_model()
model.summary()

#example = image_train[:10]
#example_result = model.predict(example)
#print(example_result)

class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')

EPOCHS = 100

history = model.fit(image_train, angle_train, epochs=EPOCHS, \
        validation_split=0.0, verbose=0, callbacks=[PrintDot()])

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error')
  plt.plot(hist['epoch'], hist['mae'],label='Train Error')
  #plt.plot(hist['epoch'], hist['val_mae'],label = 'Val Error')
  plt.ylim([0,10])
  plt.legend()

  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error')
  plt.plot(hist['epoch'], hist['mse'],label='Train Error')
  #plt.plot(hist['epoch'], hist['val_mse'],label = 'Val Error')
  plt.ylim([0,50])
  plt.legend()
  plt.show()

plot_history(history)

loss, mae, mse = model.evaluate(image_test, angle_test, verbose=2)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

open("models/saved_model.tflite", 'wb').write(tflite_model)

#model.save('models/nnkeras_model.h5')
#tf.saved_model.save(model, 'models/nn_model')#, save_format='tf')
