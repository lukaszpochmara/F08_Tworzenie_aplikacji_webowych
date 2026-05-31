# app_4_wykresy.py
# Wykresy w Shiny for Python (matplotlib)
# Uruchom: shiny run --reload app_4_wykresy.py

import matplotlib.pyplot as plt
import numpy as np
from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.h2("Wykresy w Shiny for Python"),

    ui.row(
        ui.column(4,
            ui.h4("Ustawienia"),
            ui.input_slider("n", "Liczba punktow:", min=10, max=500, value=100),
            ui.input_slider("srednia", "Srednia:", min=-5, max=5, value=0),
            ui.input_slider("odch", "Odchylenie std.:", min=0.1, max=5.0, value=1.0),
            ui.input_select("typ", "Typ wykresu:",
                            choices=["Histogram", "Wykres rozrzutu", "Wykres liniowy"]),
            ui.input_select("kolor", "Kolor:",
                            choices=["steelblue", "firebrick", "seagreen", "darkorange"]),
        ),
        ui.column(8,
            ui.h4("Wykres"),
            ui.output_plot("wykres"),
        )
    ),

    ui.hr(),
    ui.h4("Statystyki"),
    ui.output_code("statystyki"),
)

def server(input, output, session):

    @output()
    @render.plot
    def wykres():
        np.random.seed(42)
        dane = np.random.normal(input.srednia(), input.odch(), input.n())

        fig, ax = plt.subplots(figsize=(7, 4))
        kolor = input.kolor()

        if input.typ() == "Histogram":
            ax.hist(dane, bins=20, color=kolor, edgecolor="white", alpha=0.8)
            ax.set_xlabel("Wartosc")
            ax.set_ylabel("Liczba")
            ax.set_title(f"Histogram (n={input.n()})")

        elif input.typ() == "Wykres rozrzutu":
            x = np.arange(input.n())
            ax.scatter(x, dane, color=kolor, alpha=0.5, s=10)
            ax.axhline(y=input.srednia(), color="red",
                       linestyle="--", label="Srednia")
            ax.set_xlabel("Indeks")
            ax.set_ylabel("Wartosc")
            ax.set_title(f"Wykres rozrzutu (n={input.n()})")
            ax.legend()

        elif input.typ() == "Wykres liniowy":
            x = np.arange(input.n())
            ax.plot(x, dane, color=kolor, alpha=0.7, linewidth=0.8)
            ax.axhline(y=input.srednia(), color="red",
                       linestyle="--", label="Srednia")
            ax.set_xlabel("Indeks")
            ax.set_ylabel("Wartosc")
            ax.set_title(f"Wykres liniowy (n={input.n()})")
            ax.legend()

        plt.tight_layout()
        return fig

    @output()
    @render.code
    def statystyki():
        np.random.seed(42)
        dane = np.random.normal(input.srednia(), input.odch(), input.n())
        return (
            f"Liczba punktow : {input.n()}\n"
            f"Srednia        : {np.mean(dane):.4f}\n"
            f"Mediana        : {np.median(dane):.4f}\n"
            f"Odch. std.     : {np.std(dane):.4f}\n"
            f"Min            : {np.min(dane):.4f}\n"
            f"Max            : {np.max(dane):.4f}"
        )

app = App(app_ui, server)
