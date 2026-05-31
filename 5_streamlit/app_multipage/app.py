import streamlit as st
import os

# 1. Konfiguracja strony - MUSI być pierwsza
st.set_page_config(
    page_title="Moja Aplikacja",
    layout="wide"
)

# 2. Logo w pasku bocznym
st.sidebar.image(
    os.path.join(os.path.dirname(__file__), "wne_uw.png"),
    width=180
)
st.sidebar.markdown("---")

# 3. Logo na stronie głównej
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(
        os.path.join(os.path.dirname(__file__), "wne_uw.png"),
        width=300
    )

# 4. Treść strony
st.title("Strona główna")
st.write("Wybierz sekcję z menu po lewej stronie.")

st.markdown("""
### Dostępne sekcje:
- **Dane** — wczytaj i przejrzyj swój zbiór danych
- **Wykresy** — wizualizacje i wykresy
- **O aplikacji** — informacje o projekcie
""")

st.info("Ta aplikacja demonstruje układ wielostronicowy w Streamlit.")