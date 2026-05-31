# app_3_reaktywnosc.py
# Reaktywnosc w Shiny for Python
# Uruchom: shiny run --reload app_3_reaktywnosc.py

from shiny import App, ui, render, reactive

app_ui = ui.page_fluid(
    ui.h2("Reaktywnosc w Shiny"),
    ui.p("Zmien suwak — wyniki aktualizuja sie automatycznie!"),

    ui.hr(),

    ui.row(
        ui.column(6,
            ui.h4("Dane wejsciowe"),
            ui.input_slider("liczba", "Wybierz liczbe:", min=1, max=20, value=5),
            ui.input_select("operacja", "Wybierz operacje:",
                            choices=["Kwadrat", "Szescian", "Pierwiastek", "Podwoj"]),
        ),
        ui.column(6,
            ui.h4("Wynik"),
            ui.output_code("wynik"),
            ui.output_text("opis"),
        )
    ),

    ui.hr(),

    ui.h4("Historia obliczen (ostatnie 5)"),
    ui.output_text("historia_text"),
)

def server(input, output, session):

    # Reaktywna wartosc — przechowuje liste wynikow
    historia_val = reactive.Value([])

    @reactive.calc
    def oblicz():
        n = input.liczba()
        op = input.operacja()
        if op == "Kwadrat":
            return n ** 2
        elif op == "Szescian":
            return n ** 3
        elif op == "Pierwiastek":
            return round(n ** 0.5, 4)
        elif op == "Podwoj":
            return n * 2

    @reactive.effect
    def zapisz_do_historii():
        wynik = oblicz()
        n = input.liczba()
        op = input.operacja()
        wpis = f"{op}({n}) = {wynik}"
        aktualna = historia_val.get()
        historia_val.set((aktualna + [wpis])[-5:])

    @output()
    @render.code
    def wynik():
        return f"Wynik: {oblicz()}"

    @output()
    @render.text
    def opis():
        return f"Operacja: {input.operacja()} na liczbie {input.liczba()}"

    @output()
    @render.text
    def historia_text():
        wpisy = historia_val.get()
        if not wpisy:
            return "Brak historii — przesuń suwak!"
        return "\n".join(reversed(wpisy))

app = App(app_ui, server)
