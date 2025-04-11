# import sys
# import os

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))


# Import packages
import json
from dash import Dash, html, dcc, callback, Output, Input, State, ctx, ALL, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
from .classes.Unit import Unit
from .classes.Pool import Pool
from .classes.Shop import Shop
from .classes.util import number_shops, n_other_shop_distribution, n_pool_shop_distribution

pool = Pool()
shops = [Shop(i) for i in range(1,12)]

# Initialize the app - incorporate css
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "TFT Rolling: Expected Number of Rolls"

server = app.server

cost_colors = ['secondary', 'success','primary', '4-cost', 'warning']

unit_collapse_buttons = html.Div(
    dbc.Container(
        [ 
            dbc.Button(
                f"{i}",
                id={'type': 'collapse-btn', 'cost': i},
                className="me-1",
                n_clicks=0,
                color=[cost_colors[i-1]],
                outline=True,
                style={'width': '18%'},
            ) for i in range(1, 6)
        ]
    )
)

collapse_group = dbc.Container([
    dbc.Collapse([
        dbc.Button(
            unit_name, 
            id={
                'index':unit_name, 
                'type': 'btn-unit', 
                'cost':i
                }, 
            color=[cost_colors[i-1]], 
            outline=True, 
            className="me-1", 
            n_clicks=0) 
        for unit_name in sorted(pool.unit_dict[i])
        ],
        id={'type': 'collapse', 'cost': i},
        is_open=False) 
    for i in range (1, 6)
])

controls = html.Div([
    html.Div(
        children=[
            html.P('Select a unit and cost (default is random 4-cost)'),
            unit_collapse_buttons,
            html.Br(),
            collapse_group,
            dcc.Store('selected-unit', 
                      data=json.dumps({
                          'unit_name': '4-cost Unit',
                          'cost': 4
                      })),
            html.Br(),
            html.P('Star level of desired unit'),
            dcc.Dropdown(
                options=[1, 2, 3], 
                value=2, 
                id='star-level'),
            html.Br(),
            html.P('Level'),
            dcc.Dropdown(
                options=list(range(1, 11)), 
                value=8, 
                id='level'),
            html.Br(),
            html.P("Number of desired unit you've already purchased"),
            dcc.Dropdown(
                options=list(range(8)), 
                value=0, 
                id='nteam'),
            html.Br(),
            html.P('Number of desired unit on other boards and benches'),
            dbc.Input(
                placeholder='Integer (0+)', 
                type='number',
                value=0, 
                id='nother'),
            html.Br(),
            html.P('Number of others units of the same cost out of the pool'),
            dbc.Input(
                placeholder='Integer (0+)', 
                type='number',
                value=0, 
                id='n_out_of_pool'),
            html.Br(),
            html.Br(),
            html.Div(
                dbc.Button(
                    'Submit',
                    # [dbc.Spinner(size="sm"), " Loading..."],
                    id='submit-val', 
                    n_clicks=0),
                className="d-grid gap-2 col-12 mx-auto"
            ),

        ]
    )
])

output = dbc.Card(
    [
        dbc.Container([
            html.Br(),
            html.Div(id='roll-string', children=''),
            html.Br(),
            ]),
        # dbc.CardHeader()
        dbc.Container(
            dbc.Tabs([
                dbc.Tab(
                    dcc.Graph(id='n-other-plot'), 
                    label='Units Held'),
                dbc.Tab(
                    dcc.Graph(id='n-pool-plot'),
                    label='Pool Size'
                    )
            ])
        )
        
    ])



app.layout = dbc.Container([
    html.Div(className='row',children='TFT: Expected Number of Rolls', style = {'textAlign': 'center', 'fontSize': 30}),
    html.Hr(),
    dbc.Row([
        dbc.Col(controls, width=4),
        dbc.Col(output, width=8)  
        ]),
    ])
@callback(
    Output(component_id='roll-string', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='nother', component_property='value'),
    State(component_id='n_out_of_pool', component_property='value'),
    State(component_id='level', component_property='value'),
)
def update_number_of_shops(n_clicks, unit_data, star_level, nteam, nother, n_out_of_pool, level):
    
    text = 'Expected # of shops:'

    if n_clicks > 0:
        unit_data = json.loads(unit_data)
        text = 'Expected # of shops until {} {} star: {}'.format(
            unit_data['unit_name'],
            star_level,
            number_shops(
                Unit(unit_data['unit_name'], unit_data['cost']), 
                nteam=nteam, 
                npool=pool.size(unit_data['cost']) - n_out_of_pool - nteam - nother, 
                nother=nother, 
                star=star_level,
                level=level, 
                shop=shops[level-1],
                disable_print=True
                )
            )

    return text

@callback(
    Output(component_id='n-other-plot', component_property='figure'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='n_out_of_pool', component_property='value'),
    State(component_id='level', component_property='value'),
)
def n_other_plot(n_clicks, unit_data, star_level, nteam, n_out_of_pool, level):
    
    if n_clicks > 0:
        unit_data = json.loads(unit_data)
        fig = n_other_shop_distribution(
            Unit(unit_data['unit_name'], unit_data['cost']), 
            nteam=nteam, 
            npool=pool.size(unit_data['cost']) - n_out_of_pool - nteam, 
            star=star_level,
            level=level, 
            shop=shops[level-1]
        )
    else:
        fig = px.line()
        fig.update_layout(
            xaxis_title="# of unit left in pool",
            yaxis_title="Expected # of shops",
            title="Effect of # left in pool on expected # of shops",
            template="simple_white"
        )
        fig.update_traces(hovertemplate="# Left: %{x}<br>Expected # Shops: %{y}")
   

    return fig

@callback(
    Output(component_id='n-pool-plot', component_property='figure'),
    Input(component_id='submit-val', component_property='n_clicks'),
    State(component_id='selected-unit', component_property='data'),
    State(component_id='star-level', component_property='value'),
    State(component_id='nteam', component_property='value'),
    State(component_id='nother', component_property='value'),
    State(component_id='level', component_property='value'),
)
def n_pool_plot(n_clicks,unit_data, star_level, nteam, nother, level):
    
    if n_clicks > 0:
        unit_data = json.loads(unit_data)
        fig = n_pool_shop_distribution(
            Unit(unit_data['unit_name'], unit_data['cost']), 
            nteam=nteam, 
            nother=nother, 
            star=star_level,
            level=level, 
            shop=shops[level-1],
            units_per_cost=len(set(unit.name for unit in pool.units[unit_data['cost']]))
        )
    else:
        fig = px.line()
        fig.update_layout(
            xaxis_title="# of other same-costs left in pool",
            yaxis_title="Expected # of shops",
            title="Effect of same-cost pool size on expected # of shops",
            template="simple_white"
        )
        fig.update_traces(hovertemplate="# Left: %{x}<br>Expected # Shops: %{y}")
    return fig

    
@callback(
    [Output({"type": "btn-unit", "index": ALL, "cost":ALL}, "className"),
     Output("selected-unit", "data")], 
    Input({"type": "btn-unit", "index":ALL, "cost":ALL}, "n_clicks"),
    Input({"type": "btn-unit", "index":ALL, "cost":ALL}, "id"),
    prevent_initial_call=True)
def btn_active(n_clicks, ids):
    # If no button is clicked, return default class names
    if not ctx.triggered or not any(n_clicks):
        return ["me-1" for _ in n_clicks]

    button_index = ctx.triggered_id['index']
    # Determine the active button and assign "active" class
    return [
        "me-1 active" if button_index == id_['index'] else "me-1" for id_ in ids
    ], json.dumps({'unit_name':ctx.triggered_id['index'], 'cost':ctx.triggered_id['cost']})
    
@callback(
    [Output({"type": "collapse", "cost": ALL}, "is_open"),
     Output({"type": "collapse-btn", "cost": ALL}, "className")],
    Input({"type": "collapse-btn", "cost": ALL}, "n_clicks"),
    Input({"type": "collapse-btn", "index":ALL, "cost":ALL}, "id"),
    State({"type": "collapse", "cost": ALL}, "is_open"),
    prevent_initial_call=True)
def toggle_collapse(n_clicks, collapse_btn_ids, is_open):
    # If no button is clicked, return default class names
    if not ctx.triggered or not any(n_clicks):
        return [False for _ in n_clicks], ["me-1" for _ in n_clicks]

    # Determine the active button and assign "active" class
    button_cost = ctx.triggered_id['cost']
    return [
        not is_open[i] if i == button_cost - 1 else False for i in range(5)
    ], [
        "me-1 active" if i == button_cost - 1 else "me-1" for i in range(5)
    ]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)