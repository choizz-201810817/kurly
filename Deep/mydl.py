#%%|
# keras mnist 기반의 딥러닝
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
# CNN
from keras.layers.convolutional import Conv2D, MaxPooling2D

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# %%
(X_train, Y_train), (X_test, Y_test) = keras.datasets.mnist.load_data()

# %%
# train, test
for i in range(10):
    plt.imshow(X_train[i])
    plt.show()
    print(Y_train[i])
    
# %%
