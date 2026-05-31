# Shiny for Python — Przykladowe aplikacje

## Instalacja

```
pip install shiny pandas matplotlib numpy
```

## Uruchamianie

Kazdy plik uruchamiamy w terminalu:

```
shiny run --reload nazwa_pliku.py
```

Nastepnie otwieramy przegladarke: http://127.0.0.1:8000

## Lista plikow

| Plik                  | Temat                                        |
|-----------------------|----------------------------------------------|
| app_1_hello.py        | Pierwsza aplikacja — suwak i wynik           |
| app_2_widgets.py      | Podstawowe widgety (suwak, tekst, checkbox)  |
| app_3_reaktywnosc.py  | Reaktywnosc — reactive.Calc, reactive.Value  |
| app_4_wykresy.py      | Wykresy matplotlib (histogram, scatter, linia)|
| app_5_csv.py          | Wczytywanie CSV i podstawowe EDA             |
| app_6_express.py      | Tryb Shiny Express (uproszczony)             |
| app_7_dashboard.py    | Pelny dashboard z filtrami i zakladkami      |

## Kolejnosc nauki

1. app_1_hello.py      — zacznij tutaj
2. app_2_widgets.py    — poznaj widgety
3. app_3_reaktywnosc.py — zrozum reaktywnosc
4. app_4_wykresy.py    — dodaj wykresy
5. app_5_csv.py        — wczytaj dane
6. app_6_express.py    — poznaj tryb Express
7. app_7_dashboard.py  — pelny dashboard

## Roznica: Core vs Express

### Core (app_1 do app_5, app_7)
```python
from shiny import App, ui, render

app_ui = ui.page_fluid(...)

def server(input, output, session):
    @output()
    @render.text
    def wynik():
        return "..."

app = App(app_ui, server)
```

### Express (app_6)
```python
from shiny.express import input, render, ui

ui.h2("Tytul")
ui.input_slider("n", "Liczba:", 0, 100, 50)

@render.text
def wynik():
    return f"Wybrano: {input.n()}"
```
