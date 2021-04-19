import os
import numpy as np
from PIL import Image
import tensorflow as tf

print("--hello--")

print("\n\n",os.listdir(os.getcwd()),"\n\n\n")



model_1 = tf.keras.models.load_model('model/shubh_model35.h5')

read = lambda imname: np.asarray(Image.open(imname).convert("RGB"))

def predict(imag_name):

    img = [read(imag_name)]

    img_1 = np.array(img, dtype='uint8')

    img_2 = img_1/255

    ans = model_1.predict(img_2)

    a = np.argmax(ans, axis = 1)[0]

    if a == 0:
        return "begnin"
    else:
        return "malignant"


