import streamlit as st
import time

st.title("Przykład: postęp i spinner")

# Pasek postepu
st.subheader("Pasek postepu")
st.write("Kliknij przycisk, aby zobaczyc pasek postepu.")

if st.button("Uruchom przetwarzanie"):
    st.write("Przetwarzam dane...")
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        bar.progress(i + 1)
    st.success("Przetwarzanie zakonczone!")

# Spinner
st.subheader("Spinner")
if st.button("Wczytaj raport"):
    with st.spinner("Wczytuje dane..."):
        time.sleep(2)
    st.success("Raport gotowy!")
    st.info("Znaleziono 1 240 rekordow.")
    st.warning("Uwaga: 3 rekordy maja brakujace wartosci.")
    st.error("Blad: brak dostepu do serwera (przyklad).")
