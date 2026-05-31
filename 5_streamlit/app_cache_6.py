import streamlit as st
import pandas as pd
import time

st.title("Przykład: buforowanie danych")

st.write("""
Bez `@st.cache_data` dane bylyby wczytywane od nowa przy kazdym
kliknieciu lub zmianie widgetu. Z dekoratorem — wynik jest
zapamietywany i ponownie uzywany.
""")

@st.cache_data
def wczytaj_dane(uploaded_file):
    time.sleep(2)  # symulacja dlugiego wczytywania
    return pd.read_csv(uploaded_file)

uploaded = st.file_uploader("Wgraj plik CSV")

if uploaded is not None:
    st.write("Pierwsze wczytanie zajmie 2 sekundy...")
    with st.spinner("Wczytuje..."):
        df = wczytaj_dane(uploaded)
    st.success("Dane wczytane! Kolejne uruchomienia beda natychmiastowe.")
    st.metric("Wiersze", df.shape[0])
    st.metric("Kolumny", df.shape[1])
    st.dataframe(df.head())
else:
    st.info("Wgraj plik CSV, aby zobaczyc dzialanie cache.")
