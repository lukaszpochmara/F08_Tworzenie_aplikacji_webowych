# app_5_csv.py
# Wczytywanie CSV i podstawowe EDA w Shiny for Python
# Uruchom: shiny run --reload app_5_csv.py

import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, ui, render, reactive

app_ui = ui.page_fluid(
    ui.h2("Wczytywanie CSV i EDA"),

    ui.input_file("plik", "Wgraj plik CSV:", accept=[".csv"]),

    ui.hr(),

    ui.output_ui("zawartosc"),
)

def server(input, output, session):

    @reactive.Calc
    def wczytaj_dane():
        plik = input.plik()
        if plik is None:
            return None
        return pd.read_csv(plik[0]["datapath"])

    @output()
    @render.ui
    def zawartosc():
        df = wczytaj_dane()
        if df is None:
            return ui.p("Wgraj plik CSV, aby zobaczyc dane.")

        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(exclude="number").columns.tolist()

        return ui.div(
            # Metryki
            ui.h4("Podstawowe informacje"),
            ui.row(
                ui.column(3, ui.value_box(
                    "Wiersze", str(df.shape[0]), showcase=None)),
                ui.column(3, ui.value_box(
                    "Kolumny", str(df.shape[1]), showcase=None)),
                ui.column(3, ui.value_box(
                    "Kolumny numeryczne", str(len(num_cols)), showcase=None)),
                ui.column(3, ui.value_box(
                    "Braki danych", str(df.isna().sum().sum()), showcase=None)),
            ),

            ui.hr(),

            # Podglad danych
            ui.h4("Podglad danych (pierwsze 10 wierszy)"),
            ui.output_data_frame("tabela"),

            ui.hr(),

            # Statystyki opisowe
            ui.h4("Statystyki opisowe"),
            ui.output_data_frame("statystyki"),

            ui.hr(),

            # Wykres
            ui.h4("Histogram"),
            ui.row(
                ui.column(4,
                    ui.input_select("kolumna", "Wybierz kolumne:",
                                    choices=num_cols if num_cols else [""]),
                    ui.input_slider("bins", "Liczba przedzialow:", 5, 50, 20),
                ),
                ui.column(8,
                    ui.output_plot("histogram"),
                )
            ),
        )

    @output()
    @render.data_frame
    def tabela():
        df = wczytaj_dane()
        if df is None:
            return pd.DataFrame()
        return df.head(10)

    @output()
    @render.data_frame
    def statystyki():
        df = wczytaj_dane()
        if df is None:
            return pd.DataFrame()
        return df.describe().reset_index()

    @output()
    @render.plot
    def histogram():
        df = wczytaj_dane()
        if df is None or not input.kolumna():
            return None
        col = input.kolumna()
        if col not in df.columns:
            return None
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.hist(df[col].dropna(), bins=input.bins(),
                color="steelblue", edgecolor="white")
        ax.set_xlabel(col)
        ax.set_ylabel("Liczba")
        ax.set_title(f"Rozklad: {col}")
        plt.tight_layout()
        return fig

app = App(app_ui, server)
