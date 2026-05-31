import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Wykresy")
st.write("Ta strona pokazuje rozne typy wykresow.")

uploaded = st.file_uploader("Wgraj plik CSV")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    num_cols = df.select_dtypes(include="number").columns.tolist()

    if not num_cols:
        st.warning("Brak kolumn numerycznych w pliku.")
    else:
        st.subheader("Histogram")
        kolumna = st.selectbox("Wybierz kolumne:", num_cols)
        bins = st.slider("Liczba przedzialow:", 5, 50, 20)

        fig, ax = plt.subplots()
        ax.hist(df[kolumna].dropna(), bins=bins, color="#991e1e")
        ax.set_xlabel(kolumna)
        ax.set_ylabel("Liczba")
        ax.set_title(f"Rozklad: {kolumna}")
        st.pyplot(fig)

        st.subheader("Macierz korelacji")
        fig2, ax2 = plt.subplots()
        corr = df[num_cols].corr()
        im = ax2.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        ax2.set_xticks(range(len(num_cols)))
        ax2.set_yticks(range(len(num_cols)))
        ax2.set_xticklabels(num_cols, rotation=45, ha="right")
        ax2.set_yticklabels(num_cols)
        plt.colorbar(im, ax=ax2)
        st.pyplot(fig2)
else:
    st.info("Wgraj plik CSV na stronie 'Dane', aby zobaczyc wykresy.")
