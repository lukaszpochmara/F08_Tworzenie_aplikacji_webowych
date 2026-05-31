# Streamlit - Przykladowe aplikacje

## Instalacja

```
pip install streamlit pandas matplotlib seaborn numpy
```

## Uruchamianie przykladow

Kazdy plik uruchamiamy w terminalu poleceniem:

```
streamlit run nazwa_pliku.py
```

## Lista plikow

| Plik             | Temat                              |
|------------------|------------------------------------|
| app_exp.py       | st.expander — zwijane sekcje       |
| app_metric.py    | st.metric — wskazniki KPI          |
| app_progress.py  | st.progress i st.spinner           |
| app_form.py      | st.form — formularz                |
| app_session.py   | st.session_state — pamiec sesji    |
| app_cache.py     | st.cache_data — buforowanie        |
| app_columns.py   | st.columns — uklad kolumnowy       |

## Aplikacja wielostronicowa

Folder `app_multipage/` zawiera przyklad aplikacji z wieloma stronami.

```
cd app_multipage
streamlit run app.py
```

Struktura:
```
app_multipage/
    app.py               <- strona glowna
    requirements.txt
    pages/
        1_Dane.py        <- strona z danymi
        2_Wykresy.py     <- strona z wykresami
        3_O_aplikacji.py <- opis projektu
    .streamlit/
        config.toml      <- motyw kolorystyczny
```
