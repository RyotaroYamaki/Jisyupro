import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_keras_model("nnkeras_model.h5")
tflite_model = converter.convert()
open("saved_model.tflite", 'wb').write(tflite_model)
