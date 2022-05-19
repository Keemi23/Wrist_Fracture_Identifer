import streamlit as st
from apps import login, model
from multiapp import MultiApp
import pandas as pd
import os
from PIL import Image, ImageOps
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
conn = sqlite3.connect('identifier.db', check_same_thread=False)
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(firstname TEXT,lastname TEXT,contact int ,username TEXT,password TEXT)')


def add_userdata(firstname,lastname,contact,username,password):
	c.execute('INSERT INTO userstable(firstname,lastname,contact,username,password) VALUES (?,?,?,?,?)',(firstname,lastname,contact,username,password))
	conn.commit()
 
 
def create_imagetable():
	c.execute('CREATE TABLE IF NOT EXISTS imagestable(imageID int auto_increment,name TEXT,photo LONGBLOB)')



def add_image(id,name,photo):
	c.execute('INSERT INTO imagestable(imageID,name,photo) VALUES (?,?,?)',(id,name,photo))
	conn.commit()
 

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT firstname,lastname,contact FROM userstable')
	data = c.fetchall()
	return data  

        
def create_patienttable():
	c.execute('CREATE TABLE IF NOT EXISTS patienttable(patientNumber int ,imageStatus TEXT,feedback TEXT)')
 
def add_patientdata(patientNumber,imageStatus,feedback):
	c.execute('INSERT INTO patienttable(patientNumber,imageStatus,feedback) VALUES (?,?,?)',(patientNumber,imageStatus,feedback))
	conn.commit()
              
def veiw_all_patient():
    c.execute("""SELECT * from patienttable""")
    record = c.fetchall()
    return record

def locate_patient_by_patientNumber(patientNumber):
	c.execute('SELECT * FROM patienttable WHERE patientNumber =?',(patientNumber))
	data = c.fetchall()
	return data


def locate_patient_by_imageStatus(imageStatus):
	c.execute('SELECT * FROM patienttable WHERE imageStatus =?',(imageStatus))
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

                menu = ["Choose Options Here","Analyse an Image","Store Patient Information","View Patient Data","View Users Information"]
                activity = st.selectbox("Menu",menu)
                
                if activity == "Choose Options Here":
                    st.success("Welcome {}".format(username))
                
                elif activity == "Analyse an Image":
                    st.markdown("Prediction : (Normal  or  Fracture)")
                    uploaded_files = st.file_uploader("Choose X-RAY image to be identified...", type=["png","jpg","jpeg"], accept_multiple_files = True)
                    class_btn = st.button("Identify")
                    if uploaded_files is not None:
                        for image_file in uploaded_files:
                            image = Image.open(image_file)
                            st.image(image, caption='Uploaded X-RAY.', use_column_width=True)
                        
                    if class_btn:
                        if uploaded_files is None:
                            st.error("Invalid command, please upload an image")
                        else:
                            with st.spinner('Analysing X-RAY Image....'):
                                label = identifier(image, 'WRIST.h5')
                                if label == 0:
                                    st.success("Image is identified to be:  NORMAL")
                                else:
                                    st.success("Image is identified to be:  FRACTURE")
                                time.sleep(1)
                                                        
                elif activity == "Store Patient Information":
                    st.subheader("Create New Patient Information")
                    new_patient_number = st.text_input("Patient Number")
                    new_patient_image_stauts = st.text_input("Status of Image")
                    new_feedback = st.text_input("Feedback")
                    if st.button("Save"):
                        create_patienttable()
                        add_patientdata(new_patient_number,new_patient_image_stauts,new_feedback)
                        st.success("You have successfully created the Patients Information")
                                
                elif activity == "View Patient Data":
                    st.subheader("Patient Image Info")
                    patient_result = veiw_all_patient()
                    clean2_db = pd.DataFrame(patient_result,columns=["Patient Number","Status of Image","Feedback"])
                    st.dataframe(clean2_db)
                                  
                elif activity == "View Users Information":
                    st.subheader("View Users Information")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Firstname","Lastname","Contact"])
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
            
            
            
# @st.caching.clear_cache()
def identifier(img, weights_file):
    # Load the model
    model = keras.models.load_model(weights_file)

    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # image = img
    #image sizing
    size = (224, 224)
    image = ImageOps.fit(img, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 255.0) - 1
    

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return np.argmax(prediction) # return position of the highest probability


