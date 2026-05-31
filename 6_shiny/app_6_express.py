# app_6_express.py
# Shiny EXPRESS — uproszczony tryb (bez App, ui, server)
# Uruchom: shiny run --reload app_6_express.py

from shiny.express import input, output, render, ui
import matplotlib.pyplot as plt
import numpy as np

ui.h2("Shiny Express — prosty dashboard")
ui.p("W trybie Express nie trzeba definiowac App(ui, server). Kod jest liniowy!")

ui.hr()

with ui.layout_columns():
    with ui.card():
        ui.card_header("Ustawienia")
        ui.input_slider("n", "Liczba punktow:", 10, 300, 100)
        ui.input_select("kolor", "Kolor wykresu:",
                        choices=["steelblue", "firebrick",
                                 "seagreen", "darkorange"])
        ui.input_checkbox("pokaz_srednia", "Pokaz srednia", value=True)

    with ui.card():
        ui.card_header("Wykres")

        @render.plot
        def wykres():
            np.random.seed(1)
            dane = np.random.randn(input.n())
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.hist(dane, bins=20,
                    color=input.kolor(), edgecolor="white", alpha=0.85)
            if input.pokaz_srednia():
                ax.axvline(x=np.mean(dane), color="red",
                           linestyle="--", linewidth=1.5,
                           label=f"Srednia: {np.mean(dane):.2f}")
                ax.legend()
            ax.set_xlabel("Wartosc")
            ax.set_ylabel("Liczba")
            ax.set_title(f"Histogram (n={input.n()})")
            plt.tight_layout()
            return fig

ui.hr()
ui.h4("Statystyki")

@render.code
def statystyki():
    np.random.seed(1)
    dane = np.random.randn(input.n())
    return (
        f"Srednia    : {np.mean(dane):.4f}\n"
        f"Mediana    : {np.median(dane):.4f}\n"
        f"Odch. std. : {np.std(dane):.4f}\n"
        f"Min        : {np.min(dane):.4f}\n"
        f"Max        : {np.max(dane):.4f}"
    )
