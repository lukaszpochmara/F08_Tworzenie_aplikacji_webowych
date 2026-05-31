# app_7_dashboard.py
# Pelny dashboard z paskiem bocznym i zakladkami
# Uruchom: shiny run --reload app_7_dashboard.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shiny import App, ui, render, reactive

# --- Dane demonstracyjne ---
np.random.seed(42)
N = 200
df_demo = pd.DataFrame({
    "miesiac":    np.tile(["Sty", "Lut", "Mar", "Kwi", "Maj",
                           "Cze", "Lip", "Sie", "Wrz", "Paz",
                           "Lis", "Gru"], N // 12 + 1)[:N],
    "sprzedaz":   np.random.normal(5000, 1200, N).round(2),
    "koszty":     np.random.normal(3000, 800, N).round(2),
    "klienci":    np.random.randint(10, 200, N),
    "region":     np.random.choice(["Polnoc", "Poludnie",
                                    "Wschod", "Zachod"], N),
    "kategoria":  np.random.choice(["A", "B", "C"], N),
})
df_demo["zysk"] = (df_demo["sprzedaz"] - df_demo["koszty"]).round(2)

# --- UI ---
app_ui = ui.page_sidebar(

    ui.sidebar(
        ui.h4("Filtry"),
        ui.input_select("region", "Region:",
                        choices=["Wszystkie"] + sorted(df_demo["region"].unique().tolist())),
        ui.input_select("kategoria", "Kategoria:",
                        choices=["Wszystkie"] + sorted(df_demo["kategoria"].unique().tolist())),
        ui.input_slider("min_sprzedaz", "Min. sprzedaz (zl):",
                        min=0, max=10000, value=0, step=500),
        ui.hr(),
        ui.output_text("liczba_rekordow"),
    ),

    ui.h2("Dashboard sprzedazowy"),

    # KPI
    ui.layout_columns(
        ui.value_box("Laczna sprzedaz", ui.output_text("kpi_sprzedaz")),
        ui.value_box("Sredni zysk",     ui.output_text("kpi_zysk")),
        ui.value_box("Liczba klientow", ui.output_text("kpi_klienci")),
        col_widths=[4, 4, 4],
    ),

    ui.hr(),

    # Zakladki
    ui.navset_tab(
        ui.nav_panel("Wykresy",
            ui.layout_columns(
                ui.card(
                    ui.card_header("Sprzedaz vs Koszty"),
                    ui.output_plot("wykres_scatter"),
                ),
                ui.card(
                    ui.card_header("Sprzedaz wg regionu"),
                    ui.output_plot("wykres_bar"),
                ),
                col_widths=[6, 6],
            ),
        ),

        ui.nav_panel("Dane",
            ui.card(
                ui.card_header("Tabela danych"),
                ui.output_data_frame("tabela"),
            )
        ),

        ui.nav_panel("Statystyki",
            ui.card(
                ui.card_header("Statystyki opisowe"),
                ui.output_data_frame("statystyki"),
            )
        ),
    ),
)

# --- Server ---
def server(input, output, session):

    @reactive.Calc
    def filtrowane():
        df = df_demo.copy()
        if input.region() != "Wszystkie":
            df = df[df["region"] == input.region()]
        if input.kategoria() != "Wszystkie":
            df = df[df["kategoria"] == input.kategoria()]
        df = df[df["sprzedaz"] >= input.min_sprzedaz()]
        return df

    @output()
    @render.text
    def liczba_rekordow():
        return f"Rekordow: {len(filtrowane())}"

    @output()
    @render.text
    def kpi_sprzedaz():
        return f"{filtrowane()['sprzedaz'].sum():,.0f} zl"

    @output()
    @render.text
    def kpi_zysk():
        return f"{filtrowane()['zysk'].mean():,.0f} zl"

    @output()
    @render.text
    def kpi_klienci():
        return f"{filtrowane()['klienci'].sum():,}"

    @output()
    @render.plot
    def wykres_scatter():
        df = filtrowane()
        fig, ax = plt.subplots(figsize=(5, 3.5))
        kolory = {"A": "steelblue", "B": "firebrick", "C": "seagreen"}
        for kat, grupa in df.groupby("kategoria"):
            ax.scatter(grupa["koszty"], grupa["sprzedaz"],
                       label=f"Kat. {kat}",
                       color=kolory.get(kat, "gray"),
                       alpha=0.6, s=20)
        ax.set_xlabel("Koszty (zl)")
        ax.set_ylabel("Sprzedaz (zl)")
        ax.set_title("Sprzedaz vs Koszty")
        ax.legend(fontsize=8)
        plt.tight_layout()
        return fig

    @output()
    @render.plot
    def wykres_bar():
        df = filtrowane()
        sr = df.groupby("region")["sprzedaz"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.bar(sr.index, sr.values, color="steelblue", edgecolor="white")
        ax.set_xlabel("Region")
        ax.set_ylabel("Srednia sprzedaz (zl)")
        ax.set_title("Srednia sprzedaz wg regionu")
        plt.tight_layout()
        return fig

    @output()
    @render.data_frame
    def tabela():
        return filtrowane().head(50)

    @output()
    @render.data_frame
    def statystyki():
        return filtrowane()[["sprzedaz", "koszty",
                              "zysk", "klienci"]].describe().reset_index()

app = App(app_ui, server)
