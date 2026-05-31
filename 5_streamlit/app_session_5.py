import streamlit as st

st.title("Koszyk zakupow")

# Inicjalizacja stanu
if "koszyk" not in st.session_state:
    st.session_state["koszyk"] = []

if "licznik" not in st.session_state:
    st.session_state["licznik"] = 0

# Dodawanie produktow
st.subheader("Sklep")
produkt = st.selectbox("Wybierz produkt:",
             ["Jablko - 2 zl", "Banan - 1.5 zl",
              "Pomarancza - 3 zl", "Winogrona - 8 zl"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Dodaj do koszyka"):
        st.session_state["koszyk"].append(produkt)
        st.session_state["licznik"] += 1
        st.success(f"Dodano: {produkt}")

with col2:
    if st.button("Wyczysc koszyk"):
        st.session_state["koszyk"] = []
        st.session_state["licznik"] = 0
        st.info("Koszyk wyczyszczony.")

# Wyswietlanie koszyka
st.subheader("Twoj koszyk")
st.metric("Liczba produktow", st.session_state["licznik"])

if st.session_state["koszyk"]:
    for i, p in enumerate(st.session_state["koszyk"], 1):
        st.write(f"{i}. {p}")
else:
    st.write("Koszyk jest pusty.")
