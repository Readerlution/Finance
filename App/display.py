from dash import Input, Output, State, dcc, html, jupyter_dash, Dash

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Application Demographics"),
        dcc.Dropdown(
            options=["Nationality", "Age", "Education"],
            value="Nationality",
            id="demo-plots-dropdown",
        ),
        html.Div(id="demo-plots-display"),
        html.H1("Experiment"),
        html.H1("Results"),
    ]
)


if __name__ == '__main__':
    app.run()