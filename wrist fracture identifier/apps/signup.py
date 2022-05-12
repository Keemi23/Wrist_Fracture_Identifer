import streamlit as st
from apps import home, data, model, login, signup # import your app modules here



def app():
    st.title('SignUp')
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")
        app.add_app("Login", login.app)
