import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Moja pirmitywna aplikacja Streamlit",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Moja pirmitywna aplikacja Streamlit")
st.write("Wgraj plik CSV i zobacz szybkie podsumowanie danych.")

uploaded_file = st.file_uploader("Wybierz plik CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Plik został poprawnie wczytany!")

    st.subheader("Podgląd danych")
    st.dataframe(df.head())

    st.subheader("Podstawowe informacje")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Liczba wierszy", df.shape[0])

    with col2:
        st.metric("Liczba kolumn", df.shape[1])

    st.subheader("Brakujące dane")
    missing_data = df.isnull().sum()
    st.dataframe(missing_data[missing_data > 0])

    st.subheader("Podstawowe statystyki")
    st.dataframe(df.describe())

    st.subheader("Prosty wykres")

    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_columns) > 0:
        selected_column = st.selectbox(
            "Wybierz kolumnę liczbową do wykresu",
            numeric_columns
        )

        fig, ax = plt.subplots()
        ax.hist(df[selected_column].dropna(), bins=20)
        ax.set_title(f"Rozkład wartości: {selected_column}")
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Liczba obserwacji")

        st.pyplot(fig)

        st.subheader("Automatyczny opis danych")
        st.write(
            f"Kolumna **{selected_column}** ma średnią wartość "
            f"**{df[selected_column].mean():.2f}**, minimum "
            f"**{df[selected_column].min():.2f}**, maksimum "
            f"**{df[selected_column].max():.2f}**."
        )
    else:
        st.warning("W pliku nie znaleziono kolumn liczbowych do wykresu.")

else:
    st.info("Najpierw wgraj plik CSV.")