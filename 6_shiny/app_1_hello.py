# app_1_hello.py
# Pierwsza aplikacja Shiny for Python
# Uruchom: shiny run --reload app_1_hello.py

from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.h2("Witaj w Shiny for Python!"),
    ui.input_slider("n", "Wybierz liczbę:", min=0, max=100, value=20),
    ui.output_code("wynik")
)

def server(input, output, session):
    @output()
    @render.code
    def wynik():
        return f"n * 2 = {input.n() * 2}"

app = App(app_ui, server)
