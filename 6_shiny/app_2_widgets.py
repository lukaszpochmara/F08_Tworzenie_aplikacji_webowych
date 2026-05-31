# app_2_widgets.py
# Podstawowe widgety w Shiny for Python
# Uruchom: shiny run --reload app_2_widgets.py

from shiny import App, ui, render

app_ui = ui.page_fluid(
    ui.h2("Podstawowe widgety"),

    ui.hr(),

    # Suwak
    ui.h4("Suwak"),
    ui.input_slider("suwak", "Wybierz liczbę:", min=0, max=100, value=50),
    ui.output_code("wynik_suwaka"),

    ui.hr(),

    # Pole tekstowe
    ui.h4("Pole tekstowe"),
    ui.input_text("imie", "Wpisz swoje imię:", value=""),
    ui.output_text("powitanie"),

    ui.hr(),

    # Checkbox
    ui.h4("Checkbox"),
    ui.input_checkbox("pokaz", "Pokaż wiadomość", value=False),
    ui.output_text("wiadomosc"),

    ui.hr(),

    # Selectbox
    ui.h4("Lista rozwijana"),
    ui.input_select("kolor", "Wybierz kolor:",
                    choices=["Czerwony", "Zielony", "Niebieski"]),
    ui.output_text("wybrany_kolor"),

    ui.hr(),

    # Radio buttons
    ui.h4("Przyciski radiowe"),
    ui.input_radio_buttons("opcja", "Wybierz opcję:",
                           choices=["Opcja A", "Opcja B", "Opcja C"]),
    ui.output_text("wybrana_opcja"),
)

def server(input, output, session):

    @output()
    @render.code
    def wynik_suwaka():
        return f"Wybrana liczba: {input.suwak()} | Do kwadratu: {input.suwak() ** 2}"

    @output()
    @render.text
    def powitanie():
        if input.imie():
            return f"Cześć, {input.imie()}!"
        return "Wpisz imię powyżej."

    @output()
    @render.text
    def wiadomosc():
        if input.pokaz():
            return "Checkbox jest zaznaczony!"
        return ""

    @output()
    @render.text
    def wybrany_kolor():
        return f"Wybrałeś: {input.kolor()}"

    @output()
    @render.text
    def wybrana_opcja():
        return f"Wybrałeś: {input.opcja()}"

app = App(app_ui, server)
