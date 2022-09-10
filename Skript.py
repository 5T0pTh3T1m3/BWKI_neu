from sklearn.model_selection import train_test_split
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow import keras
from keras.utils.vis_utils import plot_model

data = json.loads(open('FINISHED.json').read())['preise']
X_train, X_test = train_test_split(data, test_size=0.20, shuffle=False)

plt.title("Data Plot")
plt.xlabel("Index")
plt.ylabel("Data")
plt.plot(X_train)
X_train[:5]

plt.title("Data Plot")
plt.xlabel("Index")
plt.ylabel("Data")
plt.plot(X_test)
X_test[:5]

from tensorflow.python.ops.array_ops import rank_eager_fallback
X_train_data = []
Y_train_data = []
X_test_data = []
Y_test_data = []

train_len = len(X_train)
test_len = len(X_test)

# Create the training dataset
for i in range(train_len-101):
    X_train_data.append([])
    for index in range(i,(i+100)):
      X_train_data[i].append(X_train[index])
      #print(X_train[index])

    Y_train_data.append(X_train[i + 100])

# Create the test dataset
for j in range(test_len-101):
    X_test_data.append([])
    for index in range(j,(j+100)):
      X_test_data[j].append(X_test[index])
      #print(X_test[index])

    Y_test_data.append(X_test[j + 100])

Y_train_data = np.array(Y_train_data)
Y_test_data = np.array(Y_test_data)
X_test_data = np.array(X_test_data)
X_train_data = np.array(X_train_data)
    

### Printing the training and testing shapes
import numpy

print("Training size of data = ", X_train_data.shape)
print("Training size of labels = ", Y_train_data.shape)
print("Training size of data = ", X_test_data.shape)
print("Training size of labels = ", Y_test_data.shape)

### Converting the training and testing data shapes into a 3-dimensional space to make it suitable for LSTMs


X_train_data = X_train_data.reshape(X_train_data.shape[0], X_train_data.shape[1], X_train_data.shape[2], 1)
X_test_data = X_test_data.reshape(X_test_data.shape[0], X_test_data.shape[1], X_test_data.shape[2], 1)

print(X_train_data.shape)
print(X_test_data.shape)

device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
    raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))



# Build The Architecture

with tf.device('/CPU:0'):
    model=Sequential()
    model.add(LSTM(100,return_sequences=True,input_shape=(100, 2)))
    model.add(LSTM(100,return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(2))

model.summary()

# Plot the Model



keras.utils.plot_model(model, to_file='model.png', show_layer_names=True)

# Initializing the callbacks
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard

checkpoint = ModelCheckpoint("checkpoint1.h5", monitor='val_loss', verbose=1,
                              save_best_only=True, mode='auto')

logdir='logs1'
tensorboard_Visualization = TensorBoard(log_dir=logdir)

# Model Compilation 
model.compile(loss='mean_squared_error', optimizer='adam')

# Training The Model
model.fit(X_train_data, 
          Y_train_data, 
          validation_data=(X_test_data, Y_test_data), 
          epochs=20, 
          batch_size=32, 
          verbose=1,
          callbacks=[checkpoint, tensorboard_Visualization])

train_predict = model.predict(X_train_data)
test_predict = model.predict(X_test_data)

# Transform back to original form
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# Calculate RMSE performance metrics for train and test data

import math
from sklearn.metrics import mean_squared_error

print("Train MSE = ", math.sqrt(mean_squared_error(Y_train_data, train_predict)))
print("Test MSE = ", math.sqrt(mean_squared_error(Y_test_data, test_predict)))

score = model.evaluate(
    x=X_test_data,
    y=Y_test_data)

print("score = ", score)
