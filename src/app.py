import pandas as pd
import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, State, no_update, callback
import plotly.express as px

df = px.data.gapminder()

app = Dash(__name__)

columnDefs = [
    {
        "headerName": "Country",
        "field": "country",
        "checkboxSelection": True,
        "headerCheckboxSelection": True,
    },
    {"headerName": "Continent", "field": "continent"},
    {"headerName": "Year", "field": "year"},
    {"headerName": "Life Expectancy", "field": "lifeExp"},
]


app.layout = html.Div(
    [dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
        html.Span("Copy Selected "),
        dcc.Clipboard(id="clipboard-state", style={"display": "inline-block"}),
        dag.AgGrid(
            id="clipboard-state-grid",
            columnDefs=columnDefs,
            rowData=df.to_dict("records"),
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={"rowSelection": "multiple", "animateRows": False,},
        ),
        dcc.Textarea(
            placeholder="Copy rows from the grid above and paste here to see the clipboard contents",
            id="clipboard-state-output",
            style={"width": "100%", "height": 200},
        ),
    ]
)


@callback(
    Output("clipboard-state", "content"),
    Input("clipboard-state", "n_clicks"),
    Input("clipboard-state-grid", "columnState"),
    State("clipboard-state-grid", "selectedRows"),
    prevent_initial_call=True,
)
def selected(n, col_state, selected):
    if selected is None:
        return "No selections"
    if col_state is None:
        return no_update

    dff = pd.DataFrame(selected)

    # get current column order in grid
    columns = [row["colId"] for row in col_state]
    dff = dff[columns]

    return dff.to_string()


if __name__ == "__main__":
    app.run(debug=True)