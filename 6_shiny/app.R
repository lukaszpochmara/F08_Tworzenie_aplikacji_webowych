library(shiny)

ui <- fluidPage(
  sliderInput("n", "N", min = 0, max = 100, value = 20),
  verbatimTextOutput("txt")
)

server <- function(input, output, session) {
  output$txt <- renderPrint({
    paste("n*2 is", input$n * 2)
  })
}

shinyApp(ui = ui, server = server)
