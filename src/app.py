# Import packages
from dash import Dash, html, dcc, callback, Output, Input, State, ctx
import plotly.express as px
from classes.Unit import Unit
from classes.Pool import Pool
from classes.Shop import Shop
from classes.util import number_shops

pool = Pool()
shops = [Shop(i) for i in range(1,12)]

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div(className='row',children='TFT: Expected Number of Rolls', style = {'textAlign': 'center', 'fontSize': 30}),
    html.Div(
        children=[
            html.Hr(),
            html.P('Name of Unit'),
            dcc.Input(placeholder='Unit name', type='text', id='unit-name'),
            html.P('Cost of desired unit'),
            dcc.RadioItems(options=[1, 2, 3, 4, 5], inline=True, id='unit-cost'),
            html.P('Star level of desired unit'),
            dcc.RadioItems(options=[1, 2, 3], inline=True, id='star-level'),
            html.P('Level'),
            dcc.Input(placeholder='Integer (0-10)', type='number', id='level'),
            html.P('Number of desired unit already purchased'),
            dcc.Input(placeholder='Integer (0-8)', type='number', id='nteam'),
            html.P('Number of desired unit on other boards and benches'),
            dcc.Input(placeholder='Integer (0+)', type='number', id='nother'),
            html.Br(),
            html.Br(),
            html.Div(
                html.Button('Submit', id='submit-val', n_clicks=0)
            ),
            html.Div(id='roll-string',
             children=''),
            html.Hr()
        ]
    )
])
@callback(
    Output(component_id='roll-string', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='unit-name', component_property='value'),
    State(component_id='unit-cost', component_property='value'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='nother', component_property='value'),
    State(component_id='level', component_property='value'),
    prevent_initial_call=True
)
def update_number_of_shops(n_clicks, unit_name, cost, star_level, nteam, nother, level):

    text = 'Enter a value and press submit'

    # print(button)

    if n_clicks > 0:
        text = 'Number of shops until {} {} star: {}'.format(
            unit_name,
            star_level,
            number_shops(
                Unit(unit_name, cost), 
                nteam=nteam, 
                npool=pool.size(5)-nteam-nother, 
                nother=nother, 
                star=star_level,
                level=level, 
                shop=shops[9]
                )
            )

    return text


if __name__ == '__main__':
    # app.run(debug=True)
    app.run_server(debug=True, host='0.0.0.0', port=8080)