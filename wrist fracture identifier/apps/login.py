import streamlit as st
from apps import login, model
from multiapp import MultiApp
import pandas as pd
import os
from PIL import Image, ImageOps
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import *
from tensorflow.keras import preprocessing
import time


app = MultiApp()

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('fracture_identifier.db', check_same_thread=False)
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(firstname TEXT,lastname TEXT,contact int ,username TEXT,password TEXT)')


def add_userdata(firstname,lastname,contact,username,password):
	c.execute('INSERT INTO userstable(firstname,lastname,contact,username,password) VALUES (?,?,?,?,?)',(firstname,lastname,contact,username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def app():
    menu = ["Login","SignUp"]
    choice = st.selectbox("Menu",menu)
    
    if choice == "Login":
        st.subheader("Home")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Welcome {}".format(username))
                menu = ["Select Here to Analyse Image or Veiw Users Information","Analyse an Image","Veiw Users Information"]
                activity = st.selectbox("Menu",menu)
                
                if activity == "Select Here to Analyse Image, Store Image or View Images":
                    st.info("Select Here to Analyse Image, Store Image or View Images")
                
                elif activity == "Analyse an Image":
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
                                
                                
                elif activity == "Veiw Users Information":
                    st.subheader("Veiw Users Information")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Firstname","Lastname","Contact","Username","Password"])
                    st.dataframe(clean_db)
                                

                    
                else:
                    st.info("Select Option Above")             
                
                

            else:
                st.warning("Incorrect Username/Password")

    
    else: 
        choice == "SignUp"
        st.title('SignUp')
        st.subheader("Create New Account")
        new_user_fname = st.text_input("Firstname")
        new_user_lname = st.text_input("Lastname")
        new_user_contact = st.text_input("Contact")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user_fname,new_user_lname,new_user_contact,new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            
            
            

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



def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertimage(imageId, name, photo):
    try:
        sqliteConnection = sqlite3.connect('fractureidentifier.db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_blob_query = """ INSERT INTO photo
                                  (id, name, photo) VALUES (?, ?, ?)"""

        xray = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (imageId, name, xray)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        st.write("Image is successfully stored to database")
        cursor.close()

    except sqlite3.Error as error:
        st.write ("Failed to insert image", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            

# activity == "Store Image":
#                     def insertimage(imageId, name, photo):
#                         try:
#                             sqliteConnection = sqlite3.connect('fractureidentifier.db')
#                             cursor = sqliteConnection.cursor()
#                             sqlite_insert_blob_query = """ INSERT INTO photo
#                                                     (id, name, photo) VALUES (?, ?, ?)"""

#                             xray = convertToBinaryData(photo)
#                             # Convert data into tuple format
#                             data_tuple = (imageId, name, xray)
#                             cursor.execute(sqlite_insert_blob_query, data_tuple)
#                             sqliteConnection.commit()
#                             st.write("Image is successfully stored to database")
#                             cursor.close()

#                         except sqlite3.Error as error:
#                             st.write ("Failed to insert image", error)
#                         finally:
#                             if sqliteConnection:
#                                 sqliteConnection.close()
                                


