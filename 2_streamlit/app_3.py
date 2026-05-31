import streamlit as st
st.title("Hello Streamlit!")
st.write("This is my first Streamlit app.")
number = st.slider("Pick a number", 1, 500)
st.write("Your number squared:", number**2)