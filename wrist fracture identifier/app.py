import streamlit as st
from multiapp import MultiApp
from apps import home, login # import your app modules here
import os
from PIL import Image, ImageOps



# def load_image(img):
#     im =Image.open(os.path.join(img))
#     return im

app = MultiApp()

st.markdown("""
# Distal Wrist Fracture Identifier
""")
# st.image(load_image('C:\Users\Yvonne\Desktop\multi-page-app'))

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Login", login.app)
# The main app
app.run()
