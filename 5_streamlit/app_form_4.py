import streamlit as st

st.title("Rejestracja uczestnika")

with st.form("formularz_rejestracji"):
    imie   = st.text_input("Imie i nazwisko")
    wiek   = st.number_input("Wiek",
               min_value=18, max_value=99, value=25)
    miasto = st.selectbox("Miasto",
               ["Warszawa", "Krakow", "Gdansk",
                "Wroclaw", "Poznan"])
    kurs   = st.multiselect("Wybrane kursy:",
               ["Python", "SQL", "Streamlit",
                "Machine Learning"])
    zgoda  = st.checkbox("Akceptuje regulamin")
    wyslij = st.form_submit_button("Zarejestruj")

if wyslij:
    if not zgoda:
        st.error("Musisz zaakceptowac regulamin.")
    elif not imie:
        st.error("Podaj imie i nazwisko.")
    else:
        st.success(
            f"Zarejestrowano: {imie}, {wiek} lat, {miasto}")
        st.write("Wybrane kursy:", kurs)
