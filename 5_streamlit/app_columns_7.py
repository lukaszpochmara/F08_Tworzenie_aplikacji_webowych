import streamlit as st
import pandas as pd
import numpy as np

st.title("Uklad z kolumnami")

# Kolumny z proporcjami 3:1
col_wykres, col_filtr = st.columns([3, 1])

with col_filtr:
    st.subheader("Filtry")
    n = st.slider("Liczba punktow", 10, 200, 50)
    srednia = st.slider("Srednia", -3.0, 3.0, 0.0)
    odch = st.slider("Odch. std.", 0.1, 3.0, 1.0)

with col_wykres:
    st.subheader("Wykres rozrzutu")
    dane = pd.DataFrame({
        "x": np.random.normal(srednia, odch, n),
        "y": np.random.normal(srednia, odch, n)
    })
    st.scatter_chart(dane)

# Drugi przyklad: rowne kolumny
st.divider()
st.subheader("Rowne kolumny (3 x 1/3)")

c1, c2, c3 = st.columns(3)
with c1:
    st.info("Kolumna 1\nTekst, metryki, filtry")
with c2:
    st.success("Kolumna 2\nWykresy, tabele")
with c3:
    st.warning("Kolumna 3\nOpisy, linki")
