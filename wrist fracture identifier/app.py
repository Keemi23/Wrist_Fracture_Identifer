import streamlit as st
from multiapp import MultiApp
from apps import home, login # import your app modules here
import os
from PIL import Image, ImageOps
import base64



app = MultiApp()


st.markdown("""
# Distal Wrist Fracture Identifier
""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Login", login.app)
# The main app
app.run()
