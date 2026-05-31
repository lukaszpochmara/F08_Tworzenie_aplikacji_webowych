import streamlit as st
import pandas as pd

st.title("Dane")
st.write("Ta strona pozwala wczytac i przejrzec zbior danych.")

uploaded = st.file_uploader("Wgraj plik CSV")

if uploaded is not None:
    df = pd.read_csv(uploaded)

    st.success(f"Wczytano plik: {uploaded.name}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Wiersze", df.shape[0])
    with col2:
        st.metric("Kolumny", df.shape[1])

    n = st.slider("Liczba wierszy do podgladu", 5, 50, 10)
    st.dataframe(df.head(n))

    with st.expander("Typy danych"):
        st.write(df.dtypes)

    with st.expander("Brakujace wartosci"):
        st.write(df.isna().sum())
else:
    st.info("Wgraj plik CSV, aby rozpoczac.")
