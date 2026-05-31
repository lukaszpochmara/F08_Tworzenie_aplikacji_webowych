import streamlit as st

st.title("Hello Streamlit!")
st.write("This is my first Streamlit app.")

# Slider
number = st.slider("Pick a number", 1, 10)
st.write("Your number squared:", number**2)

# Text input
name = st.text_input("Enter your name:")
st.write("Hello,", name)

# Checkbox
show_message = st.checkbox("Show a secret message")
if show_message:
    st.write("You checked the box!")

# Button
if st.button("Click me"):
    st.write("Button clicked!")

# Selectbox
color = st.selectbox("Pick a color:", ["Red", "Green", "Blue"])
st.write("You selected:", color)

# Radio buttons
choice = st.radio("Choose an option:", ["Option A", "Option B", "Option C"])
st.write("You chose:", choice)

# Number input
num = st.number_input("Enter a number:", min_value=0, max_value=100, value=10)
st.write("You typed:", num)

# Multiselect
fruits = st.multiselect("Pick some fruits:",
                        ["Apple", "Banana", "Orange", "Strawberry"])
st.write("Your selection:", fruits)

# Date input
date = st.date_input("Pick a date:")
st.write("You chose:", date)

# File uploader
uploaded = st.file_uploader("Upload a file:")
if uploaded is not None:
    st.write("File uploaded:", uploaded.name)
