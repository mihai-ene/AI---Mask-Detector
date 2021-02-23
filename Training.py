import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pickle as pkl
import cv2
import random
import os
import matplotlib.pyplot as plt

# Data set : https://github.com/cabani/MaskedFace-Net

img_array = cv2.imread("Data/WithMask/00000_Mask.jpg")
training_Data = []
directory = "Data/"
categories = ["WithMask", "NoMask"]
new_array = cv2.resize(img_array, (224, 224))

# Processing the data in order to train the model on it
def create_training_Data():
    for category in categories:
        path = os.path.join(directory, category)
        class_num = categories.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                new_array = cv2.resize(img_array, (224, 224))
                training_Data.append([new_array, class_num])
            except Exception as e:
                pass
"""
create_training_Data()
random.shuffle(training_Data)
x = [] ## Data feature
y = [] ## Label

for features,label in training_Data:
    x.append(features)
    y.append(label)

x = np.array(x).reshape(-1, 224, 224, 3)
y = np.array(y)
x = x/255.0 # Normalizing the data

pkl.dump(x,open("x.pickle","wb"))
pkl.dump(y,open("y.pickle","wb"))

x = pkl.load(open("x.pickle","rb"))
y = pkl.load(open("y.pickle","rb"))



# Training the model using Tranfer Learning 

model = tf.keras.applications.mobilenet.MobileNet() ##pre-trained model

# Removing unused layer
base_input = model.layers[0].input
base_output = model.layers[-4].output

Flat_layer = layers.Flatten()(base_output)
final_output = layers.Dense(1)(Flat_layer)
final_input = layers.Activation('sigmoid')(final_output)

new_model = keras.Model(inputs=base_input, outputs=final_output)

new_model.compile(loss="binary_crossentropy", optimizer="adam",metrics=["accuracy"])
new_model.fit(x,y, epochs=1, validation_split=0.1)
new_model.save('IA - MaskDetector.h5')

"""
def TurnWebCamOn():

    """
    This functions creates an CV2 Window and predicts if the person in front of the camera has or has not a Mask,
    using the "A - Mask Detection.h5" model, who has been trained earlier on the data set.
    """

    # Loading the model
    model = keras.models.load_model('IA - MaskDetector.h5')

    path = "haarcascade_frontalface_default.xml"
    font_scale = 1.5
    font = cv2.FONT_HERSHEY_COMPLEX


    rectangle_bgr = (255, 255, 255)
    img = np.zeros((500,500))
    text = ""
    (text_width, text_height) = cv2.getTextSize(text,font,fontScale=font_scale,thickness=1)[0]
    text_offset_x = 10
    text_offset_y = img.shape[0] - 25
    box_coords = ((text_offset_x,text_offset_y),(text_offset_x + text_width + 2,text_offset_y - text_height - 2))
    cv2.rectangle(img,box_coords[0],box_coords[1],rectangle_bgr,cv2.FILLED)
    cv2.putText(img,text,(text_offset_x,text_offset_y),font, fontScale=font_scale,color=(0,0,0),thickness=1)
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Webcam Error")

    ok_flag = True
    while ok_flag:
        ret, frame = cap.read()
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)
        for x,y,w,h in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            cv2.rectangle(frame,(x, y), (x+w, y+h), (0,0,0),2)
            facess = faceCascade.detectMultiScale(roi_gray)
            if len(facess) == 0:
                print("No face detected")
            else:
                for (ex,ey,ew,eh) in facess:
                    face_roi = roi_color[ey: ey+eh, ex:ex + ew]
        final_image = cv2.resize(face_roi,(224,224))
        final_image = np.expand_dims(final_image, axis=0)
        final_image = final_image/255.0
        font = cv2.FONT_HERSHEY_SIMPLEX
        predictions = model.predict(final_image)
        if predictions > 0:
            status = "NOT OK!"
            print(status)
        else:
            status = "OK!"
            print(status)
        cv2.imshow('Stay Safe - Mask Detector', frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            ok_flag = False
            break
    cap.release()
    cv2.destroyWindow("Stay Safe - Mask Detector")

if __name__ == "__main__":
    TurnWebCamOn()
