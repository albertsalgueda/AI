import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow_hub as hub

#for draewing into an image
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# For measuring the inference time.
import time

image_path = ''
protxt_path = ''
model_path = ''
min_confidence = 0.35

classes = []

IMG_SHAPE = (128, 128, 3)
#model = tf.keras.applications.MobileNetV2(IMG_SHAPE,include_top=True,weights="imagenet")
model = ResNet50(weights='imagenet')

img_path = 'elephant.jpeg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
# decode the results into a list of tuples (class, description, probability)
# (one such list for each sample in the batch)
label = decode_predictions(preds, top=1)[0][0][1]
confidence = decode_predictions(preds, top=1)[0][0][2]
print(label,confidence)
