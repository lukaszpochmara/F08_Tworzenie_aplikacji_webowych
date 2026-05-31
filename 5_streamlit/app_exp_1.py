import streamlit as st

st.title("Przykład: st.expander")

with st.expander("Kliknij, aby zobaczyć szczegóły"):
    st.write("To jest ukryta treść.")
    st.write("Można tu umieścić tabele, wykresy itp.")

with st.expander("Metodologia"):
    st.write("Dane pochodzą z bazy GUS za lata 2020-2024.")
    st.write("Zastosowano regresję liniową.")

with st.expander("Słownik pojęć"):
    st.write("**EDA** — Exploratory Data Analysis (eksploracyjna analiza danych)")
    st.write("**KPI** — Key Performance Indicator (kluczowy wskaźnik efektywności)")
