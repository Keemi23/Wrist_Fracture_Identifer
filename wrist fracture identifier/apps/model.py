import streamlit as st
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from PIL import Image, ImageOps
# import matplotlib.pyplot as plt
# import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import *
from tensorflow.keras import preprocessing
import time
from multiapp import MultiApp


app = MultiApp()



def identifier(img, weights_file):
    # Load the model
    model = keras.models.load_model(weights_file)

    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = img
    #image sizing
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return np.argmax(prediction) # return position of the highest probability


def app():
    
    st.markdown("Prediction : (Normal  or  Fracture)")
    uploaded_file = st.file_uploader("Choose X-RAY image to be identified...", type="png")
    class_btn = st.button("Identify")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded X-RAY.', use_column_width=True)
        
    if class_btn:
        if uploaded_file is None:
            st.error("Invalid command, please upload an image")
        else:
            with st.spinner('Analysing X-RAY Image....'):
            # st.write("")
            # st.write("Identifying...")
                label = identifier(image, 'WRIST.h5')
                if label == 0:
                    st.success("Image is identified to be:  FRACTURE")
                else:
                    st.success("Image is identified to be:  NORMAL")
                time.sleep(1)
            
