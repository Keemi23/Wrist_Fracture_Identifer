import streamlit as st
from PIL import Image, ImageOps
from multiapp import MultiApp


app = MultiApp()




def app():
    st.title('Home')
    
    
    image = Image.open("C:\\Users\\Yvonne\\Desktop\\wrist fracture identifier\\LOGO.jpg")
    st.image(image, caption='Distal Wrist Fracture Identifier', use_column_width=True)


    

    st.write("""The radius is one of two forearm bones and is located on the thumb side.  
             The part of the radius connected to the wrist joint is called the distal radius. 
             When the radius breaks near the wrist, it is called a distal radius fracture. 
             [For more information.](https://www.hopkinsmedicine.org/health/conditions-and-diseases/distal-radius-fracture-wrist-fracture#:~:text=Distal%20radius%20fractures%20are%20one,cause%20of%20distal%20radius%20fractures)
             """)
    
    
    


