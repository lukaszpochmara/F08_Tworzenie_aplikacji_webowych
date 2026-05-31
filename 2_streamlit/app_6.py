import pandas as pd
import streamlit as st

def show_basic_info(df):
    st.subheader("Basic Info")
    st.write("Shape:", df.shape)
    st.write(df.dtypes)

def show_categorical_distributions(df):
    st.subheader("Categorical Distributions")
    cat_cols = df.select_dtypes('object').columns
    for col in cat_cols:          # <-- loop over columns
        st.write(f"**{col}**")
        st.write(df[col].value_counts())

uploaded = st.file_uploader("Upload your CSV")

if uploaded:
    df = pd.read_csv(uploaded)
    show_basic_info(df)
    show_categorical_distributions(df)