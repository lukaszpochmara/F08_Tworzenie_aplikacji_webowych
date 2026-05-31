import streamlit as st

st.title("Dashboard KPI")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Przychód",
              value="120 000 zł",
              delta="+8%")
with col2:
    st.metric(label="Liczba klientów",
              value=340,
              delta=-12)
with col3:
    st.metric(label="Zwroty",
              value="4%",
              delta="-1%")
